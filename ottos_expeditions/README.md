<a name="introduction"></a>

# 🏔️ Otto's Expeditions: Beginning Your Data Adventure with Ascend

Welcome, Expedition Engineer! 🌟 

Get ready to embark on **Otto's Expeditions**, an interactive journey where you'll harness the power of Ascend to build, manage, and optimize data flows for Otto's mountaineering adventures.

![Otto's Expeditions Logo](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/ottos_expeditions_logo.gif)

## 🐐 The Legend of Otto

Meet Otto, the extraordinary mountain goat who turned his passion for scaling peaks into a thriving adventure company. Born in the world's tallest mountains, Otto's uncanny ability to find the most daring paths to the summit caught the eye of human explorers. Now, **Otto's Summit Expeditions** offers unforgettable journeys to adventurers of all skill levels, combining Otto's innate mountain expertise with cutting-edge adventure planning.

## 🧗 Your Mission

As a data engineer for Otto's Summit Expeditions, you'll dive into the heart of the company's operations. You'll enhance and refine our data flows to ensure seamless expeditions and derive insightful analytics. From customer cohort analysis to weather impact predictions, your work will be crucial in taking Otto's adventures to new heights!

Are you ready to conquer **7 thrilling data expeditions**? Strap on your boots, fire up Ascend, and let's start climbing! 🏔️

## 🗺️ Table of Contents
1. [Introduction](#introduction)
2. [Gear Up: Getting Started](#gear-up-getting-started)
3. [Warm Up: Project Structure](#warm-up-project-structure)
4. [Your Expeditions](#your-expeditions)
    - [Expedition 1: Customer Cohort Analysis](#expedition-1-customer-cohort-analysis)
    - [Expedition 2: Gear Durability Analysis](#expedition-2-gear-durability-analysis)
    - [Expedition 3: Guide Performance & Summiting Success Rate](#expedition-3-guide-performance--summiting-success-rate)
    - [Expedition 4: Route Difficulty & Success Prediction](#expedition-4-route-difficulty--success-prediction)
    - [Expedition 5: Weather Impact Analysis](#expedition-5-weather-impact-analysis)
    - [Expedition 6: Customer Journey and Conversion Analysis](#expedition-6-customer-journey-and-conversion-analysis)
    - [Expedition 7: Revenue Cost Analysis](#expedition-7-revenue-cost-analysis)
5. [Troubleshooting Your Expedition](#troubleshooting-your-expedition)
6. [Join the Expedition Team](#join-the-expedition-team)
7. [Resources & Support](#resources--support)

---

<a name="gear-up-getting-started"></a>
![Gear Up](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/9.png)

## 🏁 Gear up: Getting Started
Before we make our ascent, let's make sure we're fully equipped for the journey ahead.

### 🔧 Prerequisites 
  - **A Configured Ascend Instance**: To request an instance, reach out to your Ascend.io representative. For details on how to configure and set up your Ascend instance, refer to the [Ascend.io Setup Guide](https://docs.ascend.io/gettingstarted/setup/).
    - A configured Ascend Instance includes the following:
      - Vault
      - Instance Store
      - Data Plane Connection

  - **A Git Repository**: You'll need a Git repository to clone the project into. 
    - NOTE: You will need to set up local SSH keys associated with this Git repository

### 📁 Cloning the Project into your Repository
  To get you started, clone the [Otto's Expeditions Project](https://github.com/ascend-io/ascend-community/tree/main/ottos_expeditions) into your repository. 

   1. In your terminal, run the following commands to clone the quickstart project:

      ```bash
      git clone git@github.com:ascend-io/ascend-community.git
      ```


   2. Clone your repository in the *same directory*:

      ```bash
      git clone {your-repo-ssh-url} # make sure you have set up local ssh keys
      cd {your-repo-name}
      ```


   3. Copy the **ottos_expeditions** project folder into your own repository:

      ```bash
      cp -r ../ascend-community/ottos_expeditions ottos_expeditions
      git add .
      git commit -m "Initial commit"
      git push
      ```


### 📝 Setting Up Your Project & Workspace

First, let's set up your Project in Ascend.

  1. Log in to your Ascend Instance and navigate to your Project Settings (steps listed below).
      - Click on your user profile in the top right
      - Click on **Settings**
      - Once the Settings menu is open, click the **Projects** tab in the sidebar.
  2. Click on **Add Project**.
  3. In the *Title* field, enter the Project title as `Otto's Expeditions`.
  4. In the *Repository* field, select the Git repository you created in the *Prerequisites* step from the dropdown menu. 
  5. In the *Project Root* field, enter the Project root directory of your repository: `ottos_expeditions`.
  6. Click **Save**.

Next, let's set up your Workspace.

  1. In the Settings page, click on the **Workspaces** tab in the sidebar.
  2. Click on **Add Workspace** and configure the workspace with the following details:

  - **Title**: `[Your Name]`
  - **Environment**: Select an Environment (e.g. `Prod`)
  - **Project**: Select the **Otto's Expeditions** Project you created in the previous step.
  - **Branch**: Create a new Branch with the name `otto/your-name-here`
  - **Base Branch**: Leave blank or select one (e.g. `main`)
  - **Profile**: Select `prod`
    - NOTE: If you see the message `Error loading profiles`, type in `prod` to the field and we will create the profile in the next step
  3. Click **Save**.

### Configuring your Profile

  1. Navigate back to your **Homepage** by clicking the Ascend icon in the top left corner.
  2. Click on the **Workspace** you just created.
  3. Click on the Files icon in the top left to open the File Explorer.
  4. Click on the Otto's Expeditions project in the File Explorer.
  5. Navigate to the `profiles` folder and click on `prod.yaml` to open the file in the editor.
  6. There are two possible configuration options presented: Azure + Snowflake, which sets parameters for your Azure Key Vault and Snowflake Data Plane, and GCP + BigQuery, which sets parameters for your GCP Secret Manager and BigQuery Data Plane. You will ***delete the set of parameters you do not need*** and then ***update the values of the set of parameters*** you will be using. You can see a sample configuration below:

  ```yaml
  profile:
    parameters:
      # TODO: If you have completed the Ascend Quickstart, you can use the same values here

      # Azure + Snowflake
      azure_key_vault_name: <your-prod-env-Azure-Key-Vault-name>
      snowflake_account: <your-prod-env-Snowflake-account-name>
      snowflake_database: ASCEND_ENV_PROD
      snowflake_schema: quickstart
      snowflake_user: ASCEND_ENV_PROD
      snowflake_role: ASCEND_ENV_PROD
      snowflake_warehouse: ASCEND_ENV_PROD
      success_rate_threshold: 50

      # GCP + BigQuery
      gcp_project_id: <your-prod-env-GCP-project-id>
      bigquery_dataset: quickstart
      success_rate_threshold: 50

    defaults:
      - kind: Flow
        name:
          regex: .*
        spec:
          data_plane:
            connection_name: my_data_plane
  ```

  7. You should now have one set of parameters (either GCP + BigQuery or Snowflake + Azure). Click **Save** to save your changes.

### Configuring your Vault

  1. Return to the open File Explorer, navigate to the `vaults` folder, and open the `my_vaults.yaml` file.
  2. Here, keep the code of the vault option you are using and delete the other.
  * If you are using GCP, delete the `azure_key_vault` block such that your file looks like this:

  ```yaml
  vault:
    gcp_secret_manager:
      project: ${parameter.gcp_project_id}
  ```
  * If you are using Azure, delete the `gcp_secret_manager` block such that your file looks like this:

  ```yaml
  vault:
    azure_key_vault:
      vault_name: ${parameter.azure_key_vault_name}
  ```

  And now you're done! You actually don't have to input the value of the vault because you did that earlier! Here's a breakdown of why (and a little bit of a sneak peek into some cool features of Ascend):
    
  * The `${}` syntax in Ascend is a way of you passing variable values around.
  * The `parameter.<vault_name>` value is being drawn from the values you set in your Profile. If you look closely, you'll notice `gcp_project_id` or `azure_key_vault_name` are values in the parameter list of the Profile you chose.

<a name="warm-up-project-structure"></a>

## 📁 Warm up: Explore the Project Structure
Now that we're all set up, let's explore the folders that make up the Otto's Expeditions Project. In your Workspace you can see all the folders and files for the project from the file explorer on the left.

- **`connections/`**: Define connections to data sources and sinks.
- **`data/`**: Host the raw data files used in the flows for this project.
- **`flows/`**: Contain the data flow definitions & components for each pipeline.
- **`profiles/`**: Define environment-specific configurations.
- **`vaults/`**: Securely manage secrets and API keys.

## 🏔️ Take on the Summits!
Now that you know your way around the project, it's time to start climbing! There are 7 expeditions in total, each designed to enhance your understanding of the Ascend platform. Think you've got what it takes to conquer them all?

Let's Ascend! 🚀

---

<a name="expedition-1-customer-cohort-analysis"></a>
![Expedition #1](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/1.png)


## 🏆 Expedition 1: Customer Cohort Analysis
**Objective**: Analyze customer cohorts to understand booking behaviors and trends.

### 1. Overview
  In this expedition, you'll work with customer data to categorize customers into cohorts and update reports for downstream consumers in PowerBI. To start, open the `flows/1-customer_cohort_analysis` folder in the File Explorer on the left.

  We'll be learning about the following concepts:
  1. How to define a basic read connector, transform, and Python task with code
  2. How to build an Ascend project with no prior working build
  3. How to run an Ascend flow

### 2. Involved Files

  We'll be using the following files in our expedition:
  - **Data Source**: 
    - `data/customers.csv`
  - **Components**: 
    - Read Connectors:
      - `customers.yaml`
    - Transforms:
      - `customer_cohort_analysis_transform.sql.jinja`
    - Python Tasks:
      - `refresh_report.py`

### 3. Flow Walkthrough
  1. **Read Component**
  
      Open `components/customers.yaml`.
    
      This simple yaml file defines the connection to our local files so we can grab customer data. We define the connection type as `local_file` and the path to the file as `customers.csv`. Note that the *name* of the connection we are using is `local_files` while the *type* of connection is `local_file`. We also define the parser as a CSV with a header.


  2. **Data Transformation**
      
      Open `components/customer_cohort_analysis_transform.sql.jinja`.

      In this simple SQL transformation component, we're transforming the data to categorize cohorts based on booking dates and behaviors.

  3. **Python Task**
      
      Open `components/refresh_report.py`.

      Our end point for this dataset is a Power BI report. This script refreshes a Power BI dataset by authenticating with Azure Active Directory and triggering the refresh through the Power BI REST API.

### 3. Run the Flow
  Now that you've explored the flow, let's run it!

  1. Since we have not built this project before, we will need to build this project.
  2. In the **Build Explorer** panel on the bottom of the screen, click on the **Build Project** button in the middle of the panel. 
      - In the case where the **Build Explorer** panel is not already open, click on **Show Build Panel** in the bottom right.
  3. Once the build completes, click on the **customer_cohort_analysis** flow on the left side of the panel.
  4. Click on the **Run** button from the Actions bar in the top right of the **Build Explorer** panel.

  You should see the flow run to completion in the **graph view** of the **Build Explorer** panel. 
  
### 4. View Run Details

  After running a flow, you may also be interested to see what the results were. To do so, you can click the **Runs** tab at the top of the **Build Explorer** panel to view details about the run including **Config Details**, **Logs**, and a **Timeline view** of the run.

  For now, we're going to focus on viewing the records that were processed in a particular run:

  1. There may be a couple runs that have an `error` status but let's click on the flow name of a run with a `success` status (the flow name is underlined).
  2. In the graph view of the run on your main panel, click on the 3 dot button at the top right of any component.
  3. From the dropdown menu that appears, select the **Records** option from the dropdown menu to see all the records going through the pipeline!

### 4. Congratulations!
  Great job! Expedition 1 was a breeze! You not only learned how to build various basic components, but you can even build and run Ascend flows now! Ready to take it to the next level? Let's try another one.

---

![Expedition #2](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/2.png)

<a name="expedition-2-gear-durability-analysis"></a>

## 🏆 Expedition 2: Gear Durability Analysis
**Objective**: Ensure the reliability of our gear by analyzing durability metrics.

### 1. Overview

  In this flow, you'll work with gear data to analyze how our gear holds up on various trips. We'll also implement data quality checks to ensure the accuracy of our data. We definitely don't want to take any risks with our gear!

  We'll be learning about the following concepts:
  1. How to write basic data quality tests in Ascend
  2. How to build an Ascend project with a previously working build

### 2. Involved Files

  To start, open the `flows/2-gear_durability_analysis` folder in the File Explorer on the left.

  - **Data Sources**: 
    - `data/expeditions.csv`
    - `data/gear_rentals.csv`
    - `data/routes.csv`
  - **Components**:
    - Read Connectors:
      - `expeditions.yaml`
      - `gear_rentals.yaml`
      - `routes.yaml`
      - `expedition_outcomes.yaml`
    - Transforms:
      - `gear_durability_analysis_transform.sql.jinja`

### 3. Flow Walkthrough
  - **Read Components**:

    In this flow we're reading data from 4 different tables. Let's take a look at each of the components for these tables:

    - Open `components/expeditions.yaml`. 
    - Open `components/gear_rentals.yaml`. 
    - Open `components/routes.yaml`. 
    - Open `components/expedition_outcomes.yaml`.
  
    These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a CSV parser that expects a header row for each CSV file.

  - **Data Transformation**:

    Open `components/gear_durability_analysis_transform.sql.jinja`.

    This query joins data from the four read components to analyze the durability of different gear types. By calculating the `damage_rate`, it provides insights into the percentage of gear that was damaged during each expedition so we can ensure we're providing our customers with reliable gear.

### 4. Add a Data Quality Test

  Let's add a data quality test to our `gear_rentals` component.

  - To add data quality tests, add the following code to the bottom of the `gear_rentals.yaml` file:

      ```yaml
        tests:
          columns:
            rental_date:
              - not_null
      ```
    With this test, we're ensuring the `rental_date` column is not null.

  - The code in `gear_rentals.yaml` should now look like the following:
      ```yaml
      component:
        read:
          connection: local_files
          local_file:
            path: /gear_rentals.csv
            parser:
              csv:
                has_header: true
        tests:
          columns:
            rental_date:
              - not_null
      ```

  - Click **Save** to save the changes.

### 5. Build & Run the Project

  Since changes have been made to the project, we will need to rebuild the project:

  1. Navigate to the bottom bar of your browser. Here, you should see a couple of items such as the build status, what branch you're on, and the last commit. 
  2. Click on the build status, which should be one of the following:
      - `No build`
      - `Build successful`
      - `Build failed`
  3. In the menu that pops up, click **Build Project**.
  4. Once the project finishes building, click on **gear_durability_analysis** in the **Build Explorer** panel and run the flow to see the results.
      - In the case where the **Build Explorer** panel is not already open, click on **Show Build Panel** in the bottom right.
  5. After the flow runs, view the records of the successful run to see how this data quality test changed which records are being processed.

### 6. Congratulations!
  
  Great job! You've completed Expedition 2! Better yet, now that you know how to create data quality checks, you can make sure your data is always clean and ready to use. Can't stop here though, let's keep climbing!

---

![Expedition #3](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/3.png)

<a name="expedition-3-guide-performance--summiting-success-rate"></a>

## 🏆 Expedition 3: Guide Performance & Summiting Success Rate
**Objective**: Evaluate guide performance and the success rates of expeditions.

### 1. Overview

  In this flow, you'll work with performance data to evaluate guide performance and the success rates of expeditions. We'll also work with Otto to update our transformation logic to create a `guide_name` field by combining first and last names. 

  We'll be learning about the following concepts:
  1. How to use Otto, your AI assistant!

### 2. Involved Files

  To start, open the `flows/3-guide_performance_summiting_success_rate` folder in the File Explorer on the left.

  - **Data Sources**: 
    - `data/expeditions.csv`
    - `data/expeditions_outcomes.csv`
    - `data/guides.csv`
  - **Components**: 
    - Read Components:
      - `expeditions.yaml`
      - `expeditions_outcomes.yaml`
      - `guides.yaml`
    - Transforms:
      - `guide_performance_summiting_success_rate_transform.sql.jinja`

### 3. Flow Walkthrough
  -  **Read Components**

      In this flow we're reading data from 3 different tables. Let's take a look at each of the components for these tables:

      - Open `components/expeditions.yaml`. 
      - Open `components/expeditions_outcomes.yaml`. 
      - Open `components/guides.yaml`. 
  
      These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a CSV parser that expects a header row for each CSV file.


  - **Data Transformation**
    
      Open `components/guide_performance_summiting_success_rate_transform.sql.jinja`.

      This query computes the success rate of each guide by analyzing their expeditions and determining how often they successfully reach the summit. The results are then ordered to highlight the guides with the highest success rates.

### 4. Update the Transformation Component

  Let's say we want to update the transformation component to create a `guide_name` field by combining first and last names. We can do this by updating the `guide_performance_summiting_success_rate_transform.sql.jinja` file to include a `guide_name` field that combines the `first_name` and `last_name` fields.

  To do this, let's try asking our trusty AI pal Otto for help.

  - Click on the **Otto** icon (it looks like a chat bubble) in the top right corner of the screen. 
  - Ask Otto to help you update the transformation component to create a `guide_name` field by combining first and last names.

      ```
      Hey Otto, can you help me update the transformation component to create a `guide_name` field by combining first and last names?
      ```

  - Otto will provide you with the code to update the transformation component. You can copy and paste the change or let Otto update the file directly for you (you just need to confirm the changes you want him to make). Below is an example of the code Otto may provide. If Otto doesn't provide something similar or is missing parts of the query, try to prompt him to fix his code for you!

    ```sql
      WITH guide_success_rate AS (
          SELECT
              g.guide_id,
              g.first_name,
              g.last_name,
              COUNT(e.expedition_id) AS total_expeditions,
              SUM(CASE WHEN eo.summit_reached = TRUE THEN 1 ELSE 0 END) AS total_successes,
              ROUND(SUM(CASE WHEN eo.summit_reached = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(e.expedition_id), 2) AS success_rate
          FROM
              {{ ref('guides') }} g
          JOIN
              {{ ref('expeditions') }} e ON g.guide_id = e.guide_id
          JOIN
              {{ ref('expedition_outcomes') }} eo ON e.expedition_id = eo.expedition_id
          GROUP BY
              g.guide_id, g.first_name, g.last_name
      )
      SELECT
          guide_id,
          first_name,
          last_name,
          total_expeditions,
          total_successes,
          success_rate
      FROM
          guide_success_rate
      ORDER BY
          success_rate DESC
    ```

  - Once the file is updated, click **Save** to save the changes.

### 5. Build & Run the Project

  As with Expedition 2, since changes have been made, we will need to rebuild the project. There's another way to build a project once you have saved new changes:

  1. If your Build Explorer panel is not open, you can open it by clicking the **Show Build Panel** button in the bottom right.
  2. Click on the **Current Build** section in the top left of the Build Explorer panel.
  3. At the top of the box to the right, you should see the line `File changes have been made since the last build`, with the **Build Project** button next to it.
  4. Click the **Build Project** button to create your new build.
  5. Once the build completes, click on **guide_performance_summiting_success_rate** in the **Build Explorer** panel and run the flow to see the results. Take a peek at the records after to see what may have changed.

### 6. Congratulations!

  Amazing! You've completed Expedition 3 and on the way, made friends with Otto, your ever helpful AI assistant! Ready for the next adventure?

---

![Expedition #4](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/4.png)
<a name="expedition-4-route-difficulty--success-prediction"></a>

## 🏆 Expedition 4: Route Difficulty & Success Prediction
**Objective**: Predict expedition success based on route difficulty.

### 1. Overview

  In this flow, you'll work with route data to predict the success of expeditions based on route difficulty. We'll also optimize the flow by changing the **materialization type** of one of the components to a **View**.

  We'll be learning about the following concepts:
  1. How to change the materialization type in a SQL query

### 2. Involved Files

  To start, open the `flows/4-route_difficulty_success_prediction` folder in the File Explorer on the left.

  - **Data Sources**: 
      - `data/expeditions_outcomes.csv`
      - `data/expeditions.csv`
      - `data/routes.csv`
  - **Components**: 
    - Read Components:
      - `expeditions_outcomes.yaml`
      - `expeditions.yaml`
      - `routes.yaml`
    - Transforms:
      - `route_difficulty_success_prediction_transform.sql.jinja`

### 3. Flow Walkthrough
  - **Read Components**

    In this flow we're reading data from 3 different tables. Let's take a look at each of the components for these tables:

    - Open `components/expeditions_outcomes.yaml`. 
    - Open `components/expeditions.yaml`. 
    - Open `components/routes.yaml`. 

    These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a CSV parser that expects a header row for each CSV file.

  - **Data Transformation**
    
    Open `components/route_difficulty_success_prediction_transform.sql.jinja`.

    The query aggregates expedition data to determine the success rate of expeditions based on the route and its difficulty level. This analysis helps us understand which routes are more challenging and how frequently expeditions successfully reach the summit.

### 4. Modify the Materialization Type

  Let's say we want to modify the materialization type of the `route_difficulty_success_prediction_transform.sql.jinja` component to a view. We can do this by changing the materialization type to `view` in the `route_difficulty_success_prediction_transform.sql.jinja` file.

  Here's how to do it:

  - Click on the `route_difficulty_success_prediction_transform.sql.jinja` file to open it.
  - Change the materialization type to `view` by inserting this code above the query.

    ```
    {{
      config(materialized="view")
    }}
    ```

  - Click **Save** to save the changes.

### 5. Build & Run the Project

  Build the project using either of the methods from Expedition 2 or 3. Once the build is complete, you can run the **route_difficulty_success_prediction** flow and view the results and records after.

### 6. Congratulations!
  
  Fantastic job making it to the end of expedition 4! The different "views" on the way to the top sure are great, huh? Let's keep going!

---

![Expedition #5](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/5.png)

<a name="expedition-5-weather-impact-analysis"></a>

## 🏆 Expedition 5: Weather Impact Analysis
**Objective**: Assess how weather conditions affect expedition outcomes.

### 1. Overview

  In this flow, you'll work with weather data to assess how weather conditions affect expedition outcomes. We'll also adjust pipeline parameters to refine weather impact insights.

  We'll be learning about the following concepts:
  1. How to change a flow's parameters

### 2. Involved Files

  To start, open the `flows/5-weather_impact_analysis` folder in the File Explorer on the left.

  - **Data Sources**: 
    - `data/expeditions_outcomes.csv`
    - `data/expeditions.csv`
    - `data/weather.csv`
  - **Components**: 
    - Read Components:
      - `expeditions_outcomes.yaml`
      - `expeditions.yaml`
      - `weather.yaml`
    - Transforms:
      - `weather_impact_analysis_transform.sql.jinja`

### 3. Flow Walkthrough

  - **Read Components**

    In this flow we're reading data from 3 different tables. Let's take a look at each of the components for these tables:

    - Open `components/expeditions_outcomes.yaml`. 
    - Open `components/expeditions.yaml`. 
    - Open `components/weather.yaml`. 
      
    These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a CSV parser that expects a header row for each CSV file.

  - **Data Transformation**
    
    Open `components/weather_impact_analysis_transform.sql.jinja`.

    This query joins data from the three read components to analyze the impact of weather conditions on expedition outcomes. By calculating the `weather_impact_rate`, it provides insights into the percentage of expeditions that were affected by weather conditions.

  One important difference between this flow and the previous ones is that we're using parameters to pass the `success_rate_threshold` to the flow at runtime (See line 21). Parameters allow us to pass variables to the flow, making it more flexible and reusable.

### 4. Adjust Pipeline Parameters

  Let's say we want to adjust the pipeline parameters to enhance analysis precision. We can do this by changing the runtime parameters for the the `weather_impact_analysis_transform.sql.jinja` file.

  To do this, we will change the `success_rate_threshold` parameter value located in the `prod.yaml` file in the `profiles` folder. Change the value from 50 to 75. The new profile should look like one of the following (the first if you used Azure/Snowflake or the second if you used GCP/BigQuery):

  ```
    # Azure + Snowflake
    azure_key_vault_name: <your-prod-env-Azure-Key-Vault-name>
    snowflake_account: <your-prod-env-Snowflake-account-name>
    snowflake_database: ASCEND_ENV_PROD
    snowflake_schema: quickstart
    snowflake_user: ASCEND_ENV_PROD
    snowflake_role: ASCEND_ENV_PROD
    snowflake_warehouse: ASCEND_ENV_PROD
    success_rate_threshold: 75
  ```
  
  OR
  
  ```
    # GCP + BigQuery
    gcp_project_id: <your-prod-env-GCP-project-id>
    bigquery_dataset: quickstart
    success_rate_threshold: 75
  ```

### 5. Build & Run the Project

  Repeat the same process as the previous expeditions to build the project. Once the build is complete, run the **weather_impact_analysis** flow to see your changes.

### 6. Congratulations!

  Sweet! You've completed Expedition 5! Plus, you now know how to use parameters in your Ascend flows, meaning you can always have the flow run with the exact specifications you want. Ready to take on the next challenge?

---

![Expedition #6](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/6.png)

<a name="expedition-6-customer-journey-and-conversion-analysis"></a>

## 🏆 Expedition 6: Customer Journey and Conversion Analysis
**Objective**: Map and optimize the customer journey to boost conversions.

### 1. Overview

  In this flow, you'll work with customer journey data to map and optimize the customer journey to help the marketing team boost conversions. We'll also implement data partitioning on our transformed data to optimize the flow.

  We'll be learning about the following concepts:
  1. How to implement Ascend Data Partitioning in a SQL transform

### 2. Involved Files

  To start, open the `6-customer_journey_conversion_analysis` folder in the File Explorer on the left.

  - **Data Sources**: 
    - `data/orders.csv`
    - `data/web_traffic.csv`
  - **Components**: 
    - Read Connectors:
      - `orders.yaml`
      - `web_traffic.yaml`
    - Transforms:
      - `customer_journey_conversion_analysis_transform.sql.jinja`

### 3. Flow Walkthrough

  - **Read Components**  

    In this flow we're reading data from 2 different tables. Let's take a look at each of the components for these tables:

    - Open `components/orders.yaml`. 
    - Open `components/web_traffic.yaml`. 

    These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a CSV parser that expects a header row for each CSV file.

  - **Data Transformation**
    
    Open `components/customer_journey_conversion_analysis_transform.sql.jinja`.

    This query joins data from the two read components to analyze the customer journey and conversion rate. By calculating the `conversion_rate`, it provides insights into the percentage of customers that converted after visiting a specific page.

### 4. Implement Data Partitioning on the Transformation Component

  Let's say we want to implement data partitioning to optimize the flow. The files we are ingesting in this flow are already partitioned by date, so we can use the partitions from upstream to partition data in the transformation component. 

  Here's how to do it:

  - Click on the `customer_journey_conversion_analysis_transform.sql.jinja` file to open it.
  - Add the following code to the file:

      ```sql  
      {{ ref('web_traffic', map_partitions=True) }} wt
      ```

  - Click **Save** to save the changes.

### 5. Build & Run the Project

  Repeat the same process as the previous expeditions to build the project. Once the build is complete, run the **customer_journey_conversion_analysis** flow to see your changes.

### 6. Congratulations!
  
  You've completed Expedition 6! That was a tricky one, but definitely a worthwhile one. You've learned about a big concept in Ascend, data partitioning, which will definitely come in handy in the future. Hold on though, your biggest adventure is still on the horizon! Ready for the final expedition?

---

![Expedition #7](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/7.png)

<a name="expedition-7-revenue-cost-analysis"></a>

## 🏆 Expedition 7: Revenue Cost Analysis
**Objective**: Analyze revenue and costs to ensure financial health.

### 1. Overview

  In this flow, you'll work with revenue and cost data to analyze the financial health of the company. Now that you've got a good grasp on the basics of the platform, you'll be building this flow from scratch. But don't worry, we've got you covered with step-by-step instructions.

  We'll be learning about the following concepts:
  1. How to create and write the code of a new Read Component
  2. How to create and write the code of a new SQL transform
  3. How to build and run your own fully functioning Ascend Flow!

  The following data will be used when you're creating your read components for this flow:

  - `data/expeditions.csv`
  - `data/financial.csv`

### 2. Set up the flow

  - **Create the flow folder**: To start, you'll need to create a new folder in the `flows` directory. Let's name it `7-revenue_cost_analysis`. This folder will host all the assets for this flow.
  - **Create the components folder**: Inside the `7-revenue_cost_analysis` folder, create a new folder called `components`. Ascend looks for a `components` folder in each flow directory to understand the components in the flow.
  - **Create the flow definition YAML**: Inside the `7-revenue_cost_analysis` folder, create a new yaml file named `7-revenue_cost_analysis.yaml`. This  file will define the flow. In advance use cases, you can use these flow definition files to define parameters for a specific flow. For now, we'll leave this empty. 

### 3. Create Your Expeditions Read Component

#### Create your Expeditions Read Component
  - Create a new file called `expeditions.yaml` in the `components` folder.
  - Open the file and add the following code:

      ```yaml
      component:
        read:
          connection: local_files
          local_file:
            path: /expeditions.csv
            parser:
              csv:
                has_header: true
      ```
    
    You'll notice that this is the same code we've used in previous flows for reading the Expeditions data. In many cases, you'll be able to reuse components from other flows so there is no need to re-ingest data. But for this flow we're keeping things simple and ingesting the data again.

  - Click **Save** to save the changes.

#### Create your Financial Read Component
  - Create a new file called `financial.yaml` in the `components` folder.
  - Open the file and add the following code:

      ```yaml
      component:
        read:
          connection: local_files
          local_file:
            path: /financial.csv
            parser:
              csv:  
                has_header: true
      ```

  - Click **Save** to save the changes.

### 4. Create Your Transformation Component
  - Create a new file called `revenue_cost_analysis_transform.sql.jinja` in the `components` folder.
  - Open the file and add the following code:

      ```sql
      WITH expedition_financials AS (
        SELECT
            e.expedition_name,
            f.total_revenue,
            f.total_cost,
            ROUND((f.total_revenue - f.total_cost) * 100.0 / f.total_revenue, 2) AS profit_margin
        FROM
          {{ ref('expeditions') }} e
        JOIN
          {{ ref('financials') }} f ON e.expedition_id = f.expedition_id
      )
      SELECT
          expedition_name,
          total_revenue,
          total_cost,
          profit_margin
      FROM
          expedition_financials
      ORDER BY
          profit_margin DESC
      ```

    This query joins data from the two read components to analyze the financial health of the company. By calculating the `profit_margin`, it provides insights into the percentage of profit margin for each expedition.

### 5. Build & Run the Project

Repeat the same process as the previous expeditions to build the project. Once the build is complete, run the **revenue_cost_analysis** flow to see your changes.

### 6. Congratulations!
Great job! You've completed Expedition 7 and made your own fully functioning Ascend flow! You did it!

---

![Congratulations!](https://storage.googleapis.com/external-docs-assets/v3/ottos-expeditions/8.png)

## Congratulations! You've completed all the expeditions!
Wow, way to go! You've successfully navigated through the challenges and conquered all the expeditions. Now you're ready to take on new adventures. Here are a few places where you can get started:

### 🧑‍🤝‍🧑 Join the Expedition Team
Become a contributor and help us scale new heights! Follow the steps in `CONTRIBUTING.md` to get started.

### 📚 Resources & Support
Enhance your knowledge and find the support you need:
- **Ask Otto**: Our integrated AI assistant can help answer questions and provide guidance. Click the chat icon in the bar at the top right of the screen.
- **Ascend.io Documentation**: [Explore here](https://docs.ascend.io)
- **Contact Us**: Reach out via [email](mailto:support@ascend.io) for personalized assistance.