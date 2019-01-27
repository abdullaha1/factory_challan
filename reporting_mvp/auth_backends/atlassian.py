from social_core.backends.atlassian import AtlassianOAuth2 as SocialAtlassianOAuth2

class AtlassianOAuth2(SocialAtlassianOAuth2):
    DEFAULT_SCOPE = ['read:jira-user', 'offline_access','read:jira-work']

    def set_access_token(self, token):
        self.access_token = token

    def get_projects(self,  *args, **kwargs):
        resources = self.get_json('https://api.atlassian.com/oauth/token/accessible-resources',
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        projects = self.get_json('https://api.atlassian.com/ex/jira/{}/rest/api/3/project?expand=description'.format(resources[0]['id']),
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        return projects

    def get_issues(self, project_id, *args, **kwargs):
        resources = self.get_json('https://api.atlassian.com/oauth/token/accessible-resources',
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        issues = self.get_json('https://api.atlassian.com/ex/jira/{}/rest/api/3/search?jql=project='.format(resources[0]['id'])+ project_id +'&maxResults=100000',
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        return issues

    def get_comments(self, issue_id, *args, **kwargs):
        resources = self.get_json('https://api.atlassian.com/oauth/token/accessible-resources',
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        comments = self.get_json("https://api.atlassian.com/ex/jira/{}/rest/api/3/issue/".format(resources[0]['id']) + issue_id + '/comment' ,
                                  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        return comments