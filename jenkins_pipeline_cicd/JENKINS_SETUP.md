# Jenkins Configuration Guide

This guide provides step-by-step instructions for setting up the Jenkins pipeline with Playwright testing.

## Prerequisites

- **Jenkins** (v2.235+) installed and running
- **Java** 11+ installed on Jenkins agent
- **Python** 3.7+ installed on Jenkins agent
- **Git** installed on Jenkins agent
- Git repository access (GitHub, GitLab, Bitbucket, etc.)

## Step 1: Install Required Jenkins Plugins

Navigate to **Manage Jenkins** → **Plugin Manager**

### Required Plugins:

1. **Pipeline** (already installed by default)
2. **Git** - For git integration
3. **HTML Publisher** - For HTML report publishing
4. **JUnit** - For test result publishing (optional)
5. **Allure** - For Allure report integration (optional)

**Installation:**
- Search for each plugin name
- Check the checkbox
- Click **Install without restart** or **Install and restart**

## Step 2: Create a New Pipeline Job

### Method 1: Using Web UI

1. Go to **Jenkins Dashboard**
2. Click **+ New Item** (or **Create a job**)
3. Enter job name: `squad-playwright-tests`
4. Select **Pipeline**
5. Click **OK**

### Method 2: Using Configuration File

Create `squad-tests.xml` in `$JENKINS_HOME/jobs/`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<org.jenkinsci.plugins.workflow.job.WorkflowJob>
  <actions/>
  <description>Playwright tests for squad accounts</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>BRANCH</name>
          <description>Git branch to checkout</description>
          <defaultValue>main</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>TESTS_PATH</name>
          <description>Path to test files (tests/smoke, tests/regression, or tests)</description>
          <defaultValue>tests/smoke</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>SQUAD_URL_FILE</name>
          <description>File containing squad account URLs</description>
          <defaultValue>squad_urls.txt</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.BooleanParameterDefinition>
          <name>HEADLESS_MODE</name>
          <description>Run Playwright in headless mode</description>
          <defaultValue>true</defaultValue>
        </hudson.model.BooleanParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition">
    <scm class="hudson.plugins.git.GitSCM">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>YOUR_REPOSITORY_URL</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</org.jenkinsci.plugins.workflow.job.WorkflowJob>
```

## Step 3: Configure Jenkins Job

### Configure Pipeline

1. Click **Configure** on your pipeline job
2. Go to **Pipeline** section
3. Choose **Pipeline script from SCM**
4. **SCM**: Select **Git**

### Git Configuration

- **Repository URL**: `https://github.com/your-org/your-repo.git`
- **Credentials**: 
  - Click **Add** → **Jenkins Credential Provider**
  - Select credential or create new one
- **Branches to build**: `*/main` (or your default branch)
- **Script Path**: `Jenkinsfile`

### Build Triggers

Optional - Configure automatic triggering:

- **GitHub hook trigger for GITScm polling** - For GitHub
- **Poll SCM** - Cron-like scheduling
  - Example: `H H * * *` (daily)

## Step 4: Configure Build Parameters

The pipeline job should have these parameters defined in the Jenkinsfile.

### To add manually:

1. Click **Configure**
2. Check **This project is parameterized**
3. Click **Add Parameter**

**Parameter 1: BRANCH**
- Type: **String Parameter**
- Name: `BRANCH`
- Default: `main`
- Description: `Git branch to checkout`

**Parameter 2: TESTS_PATH**
- Type: **Choice Parameter**
- Name: `TESTS_PATH`
- Choices: (one per line)
  ```
  tests/smoke
  tests/regression
  tests
  ```
- Description: `Path to test files`

**Parameter 3: SQUAD_URL_FILE**
- Type: **String Parameter**
- Name: `SQUAD_URL_FILE`
- Default: `squad_urls.txt`
- Description: `File containing squad account URLs`

**Parameter 4: HEADLESS_MODE**
- Type: **Boolean Parameter**
- Name: `HEADLESS_MODE`
- Default: `checked`
- Description: `Run in headless mode`

## Step 5: Configure Allure Plugin (Optional)

### Install Allure Plugin

1. **Manage Jenkins** → **Plugin Manager**
2. Search for "Allure"
3. Install "Allure plugin"

### Configure Allure in Job

1. **Configure** your pipeline job
2. Scroll to **Post-build Actions**
3. Click **Add post-build action**
4. Select **Allure Report**
5. Set **Allure Results directory**: `allure-results`

## Step 6: Configure Workspace & Build History

### Set Build Workspace

1. Click **Configure**
2. Scroll to **Advanced Project Options**
3. Set **Custom workspace root directory** (optional)
   - Example: `/var/lib/jenkins/workspace/squad-tests`

### Preserve Build History

1. Click **Configure**
2. Go to **Build History**
3. Set **Max # of builds to keep**: `20`
4. Set **Max # of builds to keep with artifacts**: `10`

## Step 7: Create Jenkins Agent Configuration (Optional)

For running on a specific agent:

### Using Agent Labels

In Jenkinsfile, specify:

```groovy
agent {
    node {
        label 'python-3.11 && playwright && linux'
    }
}
```

### Create Agent Node

1. **Manage Jenkins** → **Manage Nodes and Clouds**
2. Click **+ New Node**
3. Enter name: `playwright-agent`
4. Select **Permanent Agent**
5. Configure:
   - **# of executors**: `2`
   - **Remote root directory**: `/var/jenkins_agent`
   - **Usage**: `Only build jobs with label expressions matching this node`
   - **Labels**: `python-3.11 playwright linux`

## Step 8: Test Pipeline Execution

### Dry Run

1. Navigate to your pipeline job
2. Click **Build with Parameters**
3. Configure:
   - **BRANCH**: `main` (or your branch)
   - **TESTS_PATH**: `tests/smoke`
   - **SQUAD_URL_FILE**: `squad_urls.txt`
   - **HEADLESS_MODE**: Checked
4. Click **Build**

### Monitor Execution

1. Click **Build #1** (or latest)
2. Click **Console Output**
3. Monitor logs for:
   - Checkout success
   - Dependency installation
   - Input validation
   - Test execution
   - Report generation

## Step 9: Configure Notifications (Optional)

### Email Notifications

1. **Manage Jenkins** → **Configure System**
2. Scroll to **Extended E-mail Notification**
3. Configure SMTP settings
4. In your job, add **Post-build Actions** → **Editable Email Notification**

### Slack Notifications

1. Install **Slack plugin**
2. **Manage Jenkins** → **Configure System** → **Slack**
3. Add webhook URL
4. In your job, add **Post-build Actions** → **Slack Notification**

## Step 10: Security Configuration

### Git Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. Click **Global** → **Add Credentials**
3. Choose credential type:
   - **SSH Key** - For SSH git repos
   - **Username and password** - For HTTPS repos
4. Fill in details and save

### Jenkins URL

Set Jenkins URL for external integrations:

1. **Manage Jenkins** → **Configure System**
2. Set **Jenkins URL**: `http://your-jenkins:8080/`

## Troubleshooting

### Issue: "Jenkinsfile not found"

**Solution:**
- Verify Jenkinsfile is in repository root
- Check branch name matches configured branch
- Verify Git repository URL is correct

### Issue: "Python not found"

**Solution:**
- Install Python on Jenkins agent: `sudo apt-get install python3`
- Or configure Python in Jenkins tools

### Issue: "Permission denied" on scripts

**Solution:**
```bash
chmod +x scripts/setup.sh
chmod +x scripts/account_handler.py
```

### Issue: Test reports not generated

**Solution:**
- Verify `allure-results/` directory created
- Check Allure plugin installed
- Verify allure command available: `which allure`

## Useful Jenkins Groovy Code Snippets

### Get Build Parameters

```groovy
def branch = params.BRANCH
def testsPath = params.TESTS_PATH
def squadFile = params.SQUAD_URL_FILE
```

### Abort on Error

```groovy
if (currentBuild.result == 'FAILURE') {
    error("Build failed")
}
```

### Add Build Description

```groovy
currentBuild.description = "Tests: ${params.TESTS_PATH}, Branch: ${params.BRANCH}"
```

## Advanced: Using Jenkins Shared Libraries

Create `vars/playwrightTest.groovy`:

```groovy
def call(Map config) {
    pipeline {
        agent any
        
        stages {
            stage('Run Tests') {
                steps {
                    sh '''
                        python3 -m pytest ${config.testsPath} --alluredir=allure-results
                    '''
                }
            }
        }
    }
}
```

## Quick Reference Commands

```bash
# View Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Restart Jenkins
sudo systemctl restart jenkins

# Check Java version
java -version

# Check Python on agent
ssh jenkins@agent-host python3 --version

# Check workspace
ls -la /var/lib/jenkins/workspace/squad-tests
```

## Documentation References

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkinsfile Reference](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Declarative Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)

---

For additional support, contact your Jenkins administrator or check Jenkins logs.
