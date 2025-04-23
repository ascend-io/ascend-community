package gitops

// This package provides thin wrappers around common go‑git helpers used by the
// `oeutils` CLI.  The functions purposefully avoid terminating the process so
// that callers can decide how (and if) they want to handle failures.

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"

	git "github.com/go-git/go-git/v5"
)

// GetRepo returns the repository located at (or above) the current working
// directory together with an initialised worktree.  A clean worktree is *not*
// guaranteed – callers are expected to validate this via IsClean.
func GetRepo() (*git.Repository, *git.Worktree, error) {
	root, err := findGitRepoRoot(".")
	if err != nil {
		return nil, nil, err
	}

	repo, err := git.PlainOpen(root)
	if err != nil {
		return nil, nil, fmt.Errorf("could not open repository: %w", err)
	}

	worktree, err := repo.Worktree()
	if err != nil {
		return nil, nil, fmt.Errorf("could not get worktree: %w", err)
	}

	return repo, worktree, nil
}

// IsClean returns true if the provided worktree has no staged or unstaged
// changes.
func IsClean(worktree *git.Worktree) (bool, error) {
	status, err := worktree.Status()
	if err != nil {
		return false, fmt.Errorf("could not get worktree status: %w", err)
	}
	return status.IsClean(), nil
}

// OnMainBranch returns true if HEAD is pointing at the "main" branch.
func OnMainBranch(repo *git.Repository) (bool, error) {
	branch, err := repo.Head()
	if err != nil {
		return false, fmt.Errorf("could not get HEAD: %w", err)
	}
	return branch.Name().Short() == "main", nil
}

// findGitRepoRoot walks up the directory tree starting at `start` until a
// `.git` directory is located.  The absolute path to that directory is
// returned.
func findGitRepoRoot(start string) (string, error) {
	dir, err := filepath.Abs(start)
	if err != nil {
		return "", fmt.Errorf("could not get absolute path: %w", err)
	}

	for {
		if _, err := os.Stat(filepath.Join(dir, ".git")); err == nil {
			return dir, nil
		}

		parent := filepath.Dir(dir)
		if parent == dir { // reached filesystem root
			return "", errors.New(".git directory not found")
		}
		dir = parent
	}
}

// FindGitRoot is a tiny public wrapper around findGitRepoRoot so that other
// packages don't have to import the latter directly.
func FindGitRoot() (string, error) { return findGitRepoRoot(".") }
