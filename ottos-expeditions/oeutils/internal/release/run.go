package release

import (
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/ascend-io/ascend-community-internal/oeutils/internal/gitops"
	"github.com/ascend-io/ascend-community-internal/oeutils/internal/logger"
	"github.com/ascend-io/ascend-community-internal/oeutils/internal/unmesh"
	git "github.com/go-git/go-git/v5"
)

var (
	command      = "oeutils unmesh"
	errorMessage = `files changed after running __COMMAND__. please commit and try again.`
)

func RunRelease(push bool) {
	// Prepare git objects.
	repo, worktree, err := gitops.GetRepo()
	if err != nil {
		log.Fatalf("git setup failed: %v", err)
	}

	// 1. Run unmesh quietly so that release output only contains git status.
	silenceLogs(unmesh.RunUnmesh)

	// 2. Verify working tree is clean after unmesh before proceeding.
	clean, err := gitops.IsClean(worktree)
	if err != nil {
		log.Fatalf("could not determine worktree status: %v", err)
	}

	if !clean {
		log.Println("status is not clean:")
		status, err := worktree.Status()
		if err != nil {
			log.Fatalf("could not get status: %v", err)
		}
		for file, st := range status {
			log.Printf("\t%c%c %s", st.Staging, st.Worktree, file)
		}
		log.Fatalf("%s", strings.ReplaceAll(errorMessage, "__COMMAND__", command))
	}

	// 3. Clone the public repository into a temporary directory.
	tmpDir, err := os.MkdirTemp("", "oeutils-release-*")
	if err != nil {
		log.Fatalf("unable to create temp dir: %v", err)
	}
	publicRepoURL := "https://github.com/ascend-io/ascend-community"
	log.Printf("cloning public repository into %s", tmpDir)
	publicRepo, err := git.PlainClone(tmpDir, false, &git.CloneOptions{
		URL:      publicRepoURL,
		Progress: io.Discard,
	})
	if err != nil {
		log.Fatalf("failed to clone public repo: %v", err)
	}

	publicWT, err := publicRepo.Worktree()
	if err != nil {
		log.Fatalf("failed to get public worktree: %v", err)
	}

	// 3. Copy unmeshed projects into cloned repo.
	internalRoot, err := gitops.FindGitRoot()
	if err != nil {
		log.Fatalf("cannot find internal git root: %v", err)
	}
	srcProjects := filepath.Join(internalRoot, "projects")
	dstProjects := filepath.Join(tmpDir, "projects")

	log.Println("syncing projects directory …")
	if err := os.RemoveAll(dstProjects); err != nil && !os.IsNotExist(err) {
		log.Fatalf("failed to clean destination projects: %v", err)
	}
	if err := unmesh.CopyDirectory(srcProjects, dstProjects); err != nil {
		log.Fatalf("failed to copy projects: %v", err)
	}

	// 4. Stage all changes & commit.
	if _, err := publicWT.Add("projects"); err != nil {
		log.Fatalf("failed to stage changes: %v", err)
	}
	commitMsg := "sync from internal repo"
	if _, err := publicWT.Commit(commitMsg, &git.CommitOptions{}); err != nil {
		log.Fatalf("commit failed: %v", err)
	}
	log.Println("commit created in public repo clone")

	// 5. Push if requested.
	if push {
		log.Println("pushing to origin …")
		if err := publicRepo.Push(&git.PushOptions{}); err != nil {
			log.Fatalf("push failed: %v", err)
		}
	} else {
		log.Println("push flag not set; changes committed locally in temp clone")
	}

	// TODO: uncomment main‑branch enforcement once ready.

	// Silence staticcheck about unused variable until the enforcement is
	// implemented.
	_ = repo // lint:ignore unused until branch enforcement is added
}

// silenceLogs executes fn while discarding all output from both the standard
// logger and the package‑level `logger.Logger`. Output is restored afterwards
// so that callers can resume normal logging.
func silenceLogs(fn func()) {
	stdOrig := log.Writer()
	pkgOrig := logger.Logger.Writer()

	nullOut := io.Discard
	log.SetOutput(nullOut)
	logger.Logger.SetOutput(nullOut)

	fn()

	log.SetOutput(stdOrig)
	logger.Logger.SetOutput(pkgOrig)
}
