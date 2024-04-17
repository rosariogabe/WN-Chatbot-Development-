## Whitley-Newman (WN) Chatbot

This repository contains code for the Whitley-Newman (WN) Chatbot, an AI assistant designed to assist with insurance-related queries and interactions.

## Table of Contents
1. Introduction
2. Features
3. Installation
4. Usage
5. Configuration
6. Running the Application
7. Contributing
8. License

---

## Introduction:

The Whitley-Newman (WN) Chatbot is an AI assistant built using Streamlit and OpenAI's GPT-3.5-Turbo-16k model. It aims to provide assistance to users seeking information and guidance related to insurance policies, claims, recommendations, and other insurance-related queries.

---

## Features:

- Basic Interactions:
  - Ask about insurance policies.
  - Seek recommendations.
  - ...

- Advanced Interactions:
  - Login using Microsoft.
  - Request quotations.
  - Handle claims.
  - Assistance with product updates.
  - ...

---

## Installation:

1. Clone the repository:
   git clone https://github.com/rosariogabe/WN-Chatbot-Development-.git

2. Navigate to the project directory:
   cd WN-Chatbot-Development-

3. Install dependencies:
   pip install -r requirements.txt

---

## Usage:

To run the chatbot application, execute the following command:
streamlit run main.py

The chatbot will be accessible via a web browser at the specified URL.

---

## Configuration:

Before running the chatbot, ensure that the config.json file is properly configured with the necessary API keys and other environment variables.

---

## Cloud Environment:

### Azure OpenAI Cloud Environment Setup for GPT-3.5-Turbo-16k

To create an Azure OpenAI cloud environment for using GPT-3.5-Turbo-16k, follow these steps:

1. **Sign in to Azure Portal**: Visit [https://portal.azure.com/](https://portal.azure.com/) and sign in to your Azure account.

2. **Create a Resource Group**: Resource groups help you manage and organize your Azure resources. You can create a new resource group by navigating to "Resource groups" in the Azure Portal and clicking on "Create resource group".

3. **Create an Azure OpenAI resource**:
   - In the Azure Portal, click on "Create a resource".
   - Search for "OpenAI" in the Azure Marketplace.
   - Select the "OpenAI" resource.
   - Click on "Create" to begin the creation process.
   - Provide necessary details such as resource name, subscription, resource group, region, etc.
   - Review and confirm the configuration, then click on "Create" to deploy the resource.

4. **Configure Access and Authentication**:
   - Once the resource is deployed, navigate to the resource in the Azure Portal.
   - Configure access and authentication settings as per your requirements. This may include setting up API keys, managing authentication tokens, and defining access policies.

5. **Integration with your Application**:
   - Retrieve the API endpoint and API key from the Azure OpenAI resource you created.
   - Use the provided API endpoint and API key to integrate GPT-3.5-Turbo-16k into your application.
   - Follow the documentation provided by Microsoft for integrating Azure OpenAI into your application. This may involve using SDKs, REST APIs, or client libraries depending on your application's programming language and requirements.

6. **Testing and Optimization**:
   - Test your application to ensure that it properly integrates with Azure OpenAI and utilizes GPT-3.5-Turbo-16k as expected.
   - Optimize your application's usage of Azure OpenAI by fine-tuning parameters such as temperature, max_tokens, top_p, frequency_penalty, and presence_penalty to achieve the desired results.

7. **Monitoring and Management**:
   - Monitor the performance and usage of your Azure OpenAI resource using Azure monitoring tools.
   - Manage your resource by adjusting configurations, scaling resources up or down, and implementing security measures as needed.

## Test Environment:

A live test environment of the Whitley-Newman (WN) Chatbot is available at https://whitley-newman.streamlit.app/. You can use this environment to interact with the chatbot and test its functionalities.


## Running the Application:

To run Streamly, execute the following command:

```bash
streamlit run streamly.py

---
