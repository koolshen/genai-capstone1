"""
Support ticket functionality for creating tickets in GitHub, Trello, or Jira.
"""
import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger(__name__)

class SupportTicketManager:
    """Manages support ticket creation across different platforms."""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPO')  # Format: owner/repo
        self.trello_api_key = os.getenv('TRELLO_API_KEY')
        self.trello_token = os.getenv('TRELLO_TOKEN')
        self.trello_board_id = os.getenv('TRELLO_BOARD_ID')
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')
        self.jira_project_key = os.getenv('JIRA_PROJECT_KEY')
    
    def create_github_issue(self, title: str, body: str, labels: list = None) -> Dict[str, Any]:
        """Create a GitHub issue."""
        if not self.github_token or not self.github_repo:
            return {"error": "GitHub credentials not configured"}
        
        url = f"https://api.github.com/repos/{self.github_repo}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": body,
            "labels": labels or ["support"]
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            issue = response.json()
            logger.info(f"GitHub issue created: {issue.get('html_url')}")
            return {"success": True, "url": issue.get('html_url'), "number": issue.get('number')}
        except Exception as e:
            logger.error(f"GitHub issue creation failed: {str(e)}")
            return {"error": str(e)}
    
    def create_trello_card(self, title: str, description: str, list_id: str = None) -> Dict[str, Any]:
        """Create a Trello card."""
        if not self.trello_api_key or not self.trello_token:
            return {"error": "Trello credentials not configured"}
        
        # If no list_id provided, get the first list from the board
        if not list_id and self.trello_board_id:
            try:
                url = f"https://api.trello.com/1/boards/{self.trello_board_id}/lists"
                params = {"key": self.trello_api_key, "token": self.trello_token}
                response = requests.get(url, params=params)
                response.raise_for_status()
                lists = response.json()
                if lists:
                    list_id = lists[0]['id']
            except Exception as e:
                logger.error(f"Failed to get Trello lists: {str(e)}")
                return {"error": f"Failed to get Trello lists: {str(e)}"}
        
        if not list_id:
            return {"error": "Trello list ID not available"}
        
        url = "https://api.trello.com/1/cards"
        params = {
            "key": self.trello_api_key,
            "token": self.trello_token,
            "idList": list_id,
            "name": title,
            "desc": description
        }
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            card = response.json()
            logger.info(f"Trello card created: {card.get('url')}")
            return {"success": True, "url": card.get('url'), "id": card.get('id')}
        except Exception as e:
            logger.error(f"Trello card creation failed: {str(e)}")
            return {"error": str(e)}
    
    def create_jira_issue(self, title: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        """Create a Jira issue."""
        if not all([self.jira_url, self.jira_email, self.jira_api_token, self.jira_project_key]):
            return {"error": "Jira credentials not configured"}
        
        url = f"{self.jira_url}/rest/api/3/issue"
        auth = (self.jira_email, self.jira_api_token)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        data = {
            "fields": {
                "project": {"key": self.jira_project_key},
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, auth=auth)
            response.raise_for_status()
            issue = response.json()
            issue_url = f"{self.jira_url}/browse/{issue['key']}"
            logger.info(f"Jira issue created: {issue_url}")
            return {"success": True, "url": issue_url, "key": issue['key']}
        except Exception as e:
            logger.error(f"Jira issue creation failed: {str(e)}")
            return {"error": str(e)}
    
    def create_ticket(self, title: str, description: str, platform: str = "github") -> Dict[str, Any]:
        """Create a support ticket on the specified platform."""
        logger.info(f"Creating {platform} ticket: {title}")
        
        if platform.lower() == "github":
            return self.create_github_issue(title, description)
        elif platform.lower() == "trello":
            return self.create_trello_card(title, description)
        elif platform.lower() == "jira":
            return self.create_jira_issue(title, description)
        else:
            return {"error": f"Unsupported platform: {platform}. Supported: github, trello, jira"}

