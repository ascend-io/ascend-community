<a name="introduction"></a>

# 🏔️ Otto's Expeditions: Beginning Your Data Adventure with Ascend

Welcome, Expedition Engineer! 🌟 Get ready to embark on **Otto's Expeditions**, an interactive journey where you'll harness the power of Ascend to build, manage, and optimize data flows for Otto's mountaineering adventures.

![Otto's Expeditions Logo](/images/ottos_expeditions_logo.gif)

## 🐐 The Legend of Otto

Meet Otto, the extraordinary mountain goat who turned his passion for scaling peaks into a thriving adventure company. Born in the world's tallest mountains, Otto's uncanny ability to find the most daring paths to the summit caught the eye of human explorers. Now, **Otto's Summit Expeditions** offers unforgettable journeys to adventurers of all skill levels, combining Otto's innate mountain expertise with cutting-edge adventure planning.

## 🧗 Your Mission

As a data engineer for Otto's Summit Expeditions, you'll dive into the heart of the company's operations. You'll enhance and refine our data flows to ensure seamless expeditions and derive insightful analytics. From customer cohort analysis to weather impact predictions, your work will be crucial in taking Otto's adventures to new heights!

Are you ready to conquer **7 thrilling data expeditions?** Strap on your boots, fire up Ascend, and let's start climbing! 🏔️

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


<a name="gear-up-getting-started"></a>

## 🏁 Gear up: Getting Started
Before we make our ascent, let's make sure we're fully equipped for the journey ahead.

### 🔧 Prerequisites 
  - **A Configured Ascend Instance**: To request an instance, reach out to your Ascend.io representative. For details on how to configure and set up your Ascend instance, refer to the [Ascend.io Setup Guide](https://docs.ascend.io/gettingstarted/setup/).

  - **A Git Repository**: You'll need a Git repository to clone the project into. 


### 📁 Cloning the Project into your Repository
  To get you started, clone the [Otto's Expeditions Project](https://github.com/ascend-io/ascend-community/tree/main/ottos_expeditions) into your repository. 

   1. In your terminal, run the following commands to clone the quickstart project:

      ```bash
      git clone git@github.com:ascend-io/ascend-community.git
      ```


   2. Clone your repository in the same directory:

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

  1. Log in to your Ascend Instance and navigate to your Project Settings (**Settings** -> **Project**).
  2. Click on **Add Project**.
  3. Enter the Project Title as `Otto's Expeditions`.
  4. Select the **Git Repository** you created in the previous step. 
  5. Enter the Project Root Directory of your repository: `ottos_expeditions`.
  6. Click **Save**.

Next, let's set up your Workspace.

  1. In the settings page, click on the **Workspace** tab.
  2. Click on **Add Workspace** and configure the workspace with the following details:

  - **Workspace Title**: `[Your Name]`
  - **Environment**: Select an Environment (e.g. `Prod`)
  - **Project**: Select the **Otto's Expeditions** Project you created in the previous step.
  - **Branch**: Create a new Branch with the name `otto/your-name-here`
  - **Base Branch**: Leave blank or select one (e.g. `main`)
  - **Profile**: Select `prod`

  3. Click **Save**.

You're all set up! 🎉 To start exploring the project, open the workspace you just created. Here's how:

  1. Navigate back to your **Homepage** by clicking the Ascend icon in the top left corner.
  2. Click on the **Workspace** you just created.

<a name="warm-up-project-structure"></a>

## 📁 Warm up: Explore the Project Structure
Now that we're all set up, let's explore the folders that make up Otto's Expeditions' project. In your workspace you can see all the folders and files for the project from the file explorer on the left.

- **`connections/`**: Define connections to data sources and sinks.
- **`data/`**: Host the raw data files used in the flows for this project.
- **`flows/`**: Contain the data flow definitions & components for each pipeline.
- **`profiles/`**: Define environment-specific configurations.
- **`vaults/`**: Securely manage secrets and API keys.

## 🏔️ Take on the Summits!
Now that you know your way around the project, it's time to start climbing! There are 7 expeditions in total, each designed to enhance your understanding of the Ascend platform. Think you've got what it takes to conquer them all?

Ascend on! 🚀

---

<a name="expedition-1-customer-cohort-analysis"></a>
![Expedition #1](./images/1.png)


## 🏆 Expedition 1: Customer Cohort Analysis
**Objective**: Analyze customer cohorts to understand booking behaviors and trends.

  ### 1. Overview
  In this expedition, you'll work with customer data to categorize customers into cohorts and update reports for downstream consumers in PowerBI. To start open the `flows/customer_cohort_analysis` folder in the File Explorer on the left.

  - **Data Source**: 
    - `data/customers.csv`
  - **Components**: 
    - `customers.yaml`
    - `customer_cohort_analysis_transform.sql.jinja`
    - `refresh_powerbi.py`

  ### 2. Flow Walkthrough
  1. **Read Component**:
      - Open `components/customers.yaml`.
    
      This simple yaml file defines the connection to our local files so we can grab customer data. We define the connection type as `local_files` and the path to the file as `customers.csv`. We also define the parser as a csv with a header.


2. **Data Transformation**:
    - Open `components/customer_cohort_analysis_transform.sql.jinja`.

    In this simple SQL transformation component, we're transforming the data to categorize cohorts based on booking dates and behaviors.

  3. **Python Task**
      - Open `components/refresh_powerbi.py`.

      Our end point for this dataset is a Power BI report. This script refreshes a Power BI dataset by authenticating with Azure Active Directory and triggering the refresh through the Power BI REST API.

### 3. Run the Flow
  Now that you've explored the flow, let's run it!

  1. From the **Build Explorer** panel on the bottom of the screen click on the **customer_cohort_analysis** flow.
  2. Click on the **Run** button from the Actions bar at the top of the **Build Explorer** panel.

  You should see the flow run to completion in the **DAG view** of the **Build Explorer** panel. You can click the **Runs** tab within the **Build Explorer** panel to view details about the run including **Config Details**, **Logs**, and a **Timeline view** of the run.

### 4. Congratulations! 
  Great job! Expedition 1 was a breeze! Ready to take it to the next level? Let's try another one.

---

![Expedition #2](./images/2.png)

<a name="expedition-2-gear-durability-analysis"></a>

## 🏆 Expedition 2: Gear Durability Analysis
**Objective**: Ensure the reliability of our gear by analyzing durability metrics.

### 1. Overview
In this flow, you'll work with gear data to analyze how out gear holds up on various trips. We'll also implement data quality checks to ensure the accuracy of our data. We definitely don't want to take any risks with our gear!

To start open the `flows/gear_durability_analysis` folder in the File Explorer on the left.

- **Data Sources**: 
  - `data/expeditions.csv`
  - `data/gear_rentals.csv`
  - `data/routes.csv`
- **Components**: 
  - `expeditions.yaml`
  - `gear_durability_analysis_transform.sql.jinja`
  - `gear_rentals.yaml`
  - `routes.yaml`

### 2. Flow Walkthrough
  - **Read Components**:

      In this flow we're reading data from 3 different tables. Let's take a look at each of the components for these tables.

    - Open `components/expeditions.yaml`. 
    - Open `components/gear_rentals.yaml`. 
    - Open `components/routes.yaml`. 
  
    These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a csv with a header for each one.


  - **Data Transformation**:

    - Open `components/gear_durability_analysis_transform.sql.jinja`.

    This query joins data from the three read components to analyze the durability of different gear types. By calculating the `damage_rate`, it provides insights into the percentage of gear that was damaged during each expedition so we can ensure we're providing our customers with reliable gear.

### 3. Add Data Quality Tests

Let's add a data quality tests to our `gear_rentals` component.

  - To add a data quality tests, add the following code to the `gear_rentals.yaml` file:

      ```yaml
      tests:
        columns:
          rental_date:
            - not_null
      ```
  With this test, we're ensuring the `rental_date` column is not null.  

  - Click **Save** to save the changes.


### 4. Build the Project

To build the project with the changes you made, click on the **Build Project** button from the **Build Explorer** panel. Once the build is complete, you can run the flow to see the results.


### 5. Congratulations!
Great job! You've completed Expedition 2! Let's keep climbing.

---

![Expedition #3](./images/3.png)

<a name="expedition-3-guide-performance--summiting-success-rate"></a>

## 🏆 Expedition 3: Guide Performance & Summiting Success Rate
**Objective**: Evaluate guide performance and the success rates of expeditions.

### 1. Overview
In this flow, you'll work with performance data to evaluate guide performance and the success rates of expeditions. We'll also work with Otto to update our transformation logic to create a `guide_name` field by combining first and last names. 

To start open the `flows/guide_performance_summiting_success_rate` folder in the File Explorer on the left.

- **Data Sources**: 
  - `data/expeditions.csv`
  - `data/expeditions_outcomes.csv`
  - `data/guides.csv`
- **Components**: 
  - `expeditions.yaml`
  - `expeditions_outcomes.yaml`
  - `guide_performance_summiting_success_rate_transform.sql.jinja`
  - `guides.yaml`

### 2. Flow Walkthrough
  -  **Read Components**

      In this flow we're reading data from 3 different tables. Let's take a look at each of the components for these tables.

      - Open `components/expeditions.yaml`. 
      - Open `components/expeditions_outcomes.yaml`. 
      - Open `components/guides.yaml`. 
  
      These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a csv with a header for each one.


  - **Data Transformation**
    - Open `components/guide_performance_summiting_success_rate_transform.sql.jinja`.

    This query is to compute the success rate of each guide by analyzing their expeditions and determining how often they successfully reached the summit. The results are then ordered to highlight the guides with the highest success rates.

### 3. Update the Transformation Component

Let's say we want to update the transformation component to create a `guide_name` field by combining first and last names. We can do this by updating the `guide_performance_summiting_success_rate_transform.sql.jinja` file to include a `guide_name` field that combines the `first_name` and `last_name` fields.

To do this, let's try asking our trusty AI pal Otto for help.

  - Click on the **Otto** icon in the top right corner of the screen. (It looks like a chat bubble)
  - Ask Otto to help you update the transformation component to create a `guide_name` field by combining first and last names.

      ```
      Hey Otto, can you help me update the transformation component to create a `guide_name` field by combining first and last names?
      ```

  - Otto will provide you with the code to update the transformation component. You can copy and paste the change or let Otto update the file directly for you (you just need to confirm the changes you want him to make).
  - Once the file is updated, click **Save** to save the changes.

### 4. Build the Project

To build the project with the changes you made, click on the **Build Project** button from the **Build Explorer** panel. Once the build is complete, you can run the flow to see the results.


### 5. Congratulations!
Great job! You've completed Expedition 3! Ready for your next Adventure?

---

![Expedition #4](./images/4.png)
<a name="expedition-4-route-difficulty--success-prediction"></a>

## 🏆 Expedition 4: Route Difficulty & Success Prediction
**Objective**: Predict expedition success based on route difficulty.

### 1. Overview
In this flow, you'll work with route data to predict the success of expeditions based on route difficulty. We'll also optimize the flow by changing the **materialization type** of one of the components to a **View**.

To start open the `flows/route_difficulty_success_prediction` folder in the File Explorer on the left.

- **Data Sources**: 
    - `data/expeditions_outcomes.csv`
    - `data/expeditions.csv`
    - `data/routes.csv`

  - **Components**: 
    - `expeditions_outcomes.yaml`
    - `expeditions.yaml`
    - `routes.yaml`
    - `route_difficulty_success_prediction_transform.sql.jinja`

### 2. Flow Walkthrough
- **Read Components**
  - Open `components/expeditions_outcomes.yaml`. 
  - Open `components/expeditions.yaml`. 
  - Open `components/routes.yaml`. 

  These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a csv with a header for each one.

- **Data Transformation**
    - Open `components/route_difficulty_success_prediction_transform.sql.jinja`.

  The query aggregates expedition data to determine the success rate of expeditions based on the route and its difficulty level. This analysis helps us understand which routes are more challenging and how frequently expeditions successfully reach the summit.

### 3. Modify the Materialization Type

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

### 4. Build the Project

To build the project with the changes you made, click on the **Build Project** button from the **Build Explorer** panel. Once the build is complete, you can run the flow to see the results.

### 5. Congratulations!
Great job! You've completed Expedition 4! On to the next one!

---

![Expedition #5](./images/5.png)

<a name="expedition-5-weather-impact-analysis"></a>

## 🏆 Expedition 5: Weather Impact Analysis
**Objective**: Assess how weather conditions affect expedition outcomes.

### 1. Overview
In this flow, you'll work with weather data to assess how weather conditions affect expedition outcomes. We'll also adjust pipeline parameters to refine weather impact insights.

To start open the `flows/weather_impact_analysis` folder in the File Explorer on the left.

- **Data Sources**: 
  - `data/expeditions_outcomes.csv`
  - `data/expeditions.csv`
  - `data/weather.csv`
- **Components**: 
  - `expeditions_outcomes.yaml`
  - `expeditions.yaml`
  - `weather.yaml`
  - `weather_impact_analysis_transform.sql.jinja`

### 2. Flow Walkthrough
- **Read Components**
  - Open `components/expeditions_outcomes.yaml`. 
  - Open `components/expeditions.yaml`. 
  - Open `components/weather.yaml`. 

  These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a csv with a header for each one.

- **Data Transformation**
  - Open `components/weather_impact_analysis_transform.sql.jinja`.

  This query joins data from the three read components to analyze the impact of weather conditions on expedition outcomes. By calculating the `weather_impact_rate`, it provides insights into the percentage of expeditions that were affected by weather conditions.

  One important difference between this flow and the previous ones is that we're using parameters to pass the `success_rate_threshold` to the flow at runtime (See line 21). Parameters allow us to pass variables to the flow, making it more flexible and reusable.

### 3. Adjust Pipeline Parameters

Let's say we want to adjust the pipeline parameters to enhance analysis precision. We can do this by changing the runtime parameters for the the `weather_impact_analysis_transform.sql.jinja` file.

To do this, we will change the parameter value located in the `prod.yaml` file in the `profiles` folder. Change the value from 50 to 75.
    ```yaml
        success_rate_threshold: 75
    ```
### 4. Congratulations!
Great job! You've completed Expedition 5! Ready to take on the next challenge?

---

![Expedition #6](./images/6.png)

<a name="expedition-6-customer-journey-and-conversion-analysis"></a>

## 🏆 Expedition 6: Customer Journey and Conversion Analysis
**Objective**: Map and optimize the customer journey to boost conversions.

### 1. Overview
In this flow, you'll work with customer journey data to map and optimize the customer journey to help the marketing team boost conversions. We'll also implement data partitioning on our transformed data to optimize the flow.

To start open the `flows/customer_journey_conversion_analysis` folder in the File Explorer on the left.

- **Data Sources**: 
  - `data/orders.csv`
  - `data/web_traffic.csv`
- **Components**: 
  - `customer_journey_conversion_analysis_transform.sql.jinja`
  - `orders.yaml`
  - `web_traffic.yaml`

### 2. Flow Walkthrough
- **Read Components**
  - Open `components/orders.yaml`. 
  - Open `components/web_traffic.yaml`. 

  These components read data from our local files. We define the connection type as `local_files` and the path to the files in the data folder. We also define the parser as a csv with a header for each one.

- **Data Transformation**
  - Open `components/customer_journey_conversion_analysis_transform.sql.jinja`.

  This query joins data from the two read components to analyze the customer journey and conversion rate. By calculating the `conversion_rate`, it provides insights into the percentage of customers that converted after visiting a specific page.

### 3. Implement Data Partitioning on the Transformation Component

Let's say we want to implement data partitioning to optimize the flow. The files we are ingesting in this flow are already partitioned by date, so we can use the partitions from upstream to partition data in the transformation component. 

Here's how to do it:

- Click on the `customer_journey_conversion_analysis_transform.sql.jinja` file to open it.
- Add the following code to the file:

    ```sql  
    {{ ref('web_traffic', map_partitions=True) }} wt
    ```

- Click **Save** to save the changes.

### 4. Build the Project

To build the project with the changes you made, click on the **Build Project** button from the **Build Explorer** panel. Once the build is complete, you can run the flow to see the results.

### 5. Congratulations!
Great job! You've completed Expedition 6! Your biggest adventure is on the horizon! Ready for the final expedition?

---

![Expedition #7](./images/7.png)

<a name="expedition-7-revenue-cost-analysis"></a>

## 🏆 Expedition 7: Revenue Cost Analysis
**Objective**: Analyze revenue and costs to ensure financial health.

### 1. Overview
In this flow, you'll work with revenue and cost data to analyze the financial health of the company. Now that you've got a good grasp of the basics of the platform, you'll be building this flow from scratch. But don't worry, we've got your covered with step by step instructions.

- **Data Sources**: 
  - `data/expeditions.csv`
  - `data/financial.csv`

### 2. Set up the flow
  - To start, you'll need to create a new folder in the `flows` directory. Let's name it `revenue_cost_analysis`. This folder will host all the assets for this flow.
  - Inside the `revenue_cost_analysis` folder, create a new folder called `components`. Ascend looks for a `components` folder in each flow directory to understand the components in the flow.

### 3. Create Your Expeditions Read Component
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

  **c. Create Your Financial Read Component**
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
          profit_margin DESC;
      ```

This query joins data from the two read components to analyze the financial health of the company. By calculating the `profit_margin`, it provides insights into the percentage of profit margin for each expedition.

### 5. Build & Run the Project

To build the project with the changes you made, click on the **Build Project** button from the **Build Explorer** panel. Once the build is complete, you can run the flow to see the results.

### 6. Congratulations!
Great job! You've completed Expedition 7! 

---

![Congratulations!](./images/8.png)

## Congratulations! You've completed all the expeditions!
Great job! You've successfully navigated through the challenges and conquered all the expeditions. Now you're ready to take on new adventures. Here's a few places to start:

### 🧑‍🤝‍🧑 Join the Expedition Team
Become a contributor and help us scale new heights! Follow the steps in `CONTRIBUTING.md` to get started.

### 📚 Resources & Support
Enhance your knowledge and find the support you need:
- **Ask Otto**: Our integrated AI assistant can help answer questions and provide guidance. Click the chat icon in the bar at the top right of the screen.
- **Ascend.io Documentation**: [Explore here](https://docs.ascend.io)
- **Contact Us**: Reach out via [email](mailto:support@ascend.io) for personalized assistance.