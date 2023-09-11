import boto3

class sts_internal:
    def __init__(self, role_name) -> None:
        self.role_name = role_name
        self.client = boto3.client('sts')
        pass

    def assume_role(self):
        # Specify a session name (a name for your temporary session)
        session_name = 'dynamodb_cheat_session'

        try:
            # Assume the role
            response = self.client.assume_role(
                RoleArn=self.role_name,
                RoleSessionName=session_name
            )

            # Extract the temporary credentials
            temp_credentials = response['Credentials']

            # You can now use temp_credentials to make authenticated API calls
            # For example, create a new session with the assumed role
            assumed_role_session = boto3.Session(
                aws_access_key_id=temp_credentials['AccessKeyId'],
                aws_secret_access_key=temp_credentials['SecretAccessKey'],
                aws_session_token=temp_credentials['SessionToken']
            )

            return assumed_role_session

        except Exception as e:
            print(f"Error assuming role: {str(e)}")
            return

    def get_identity_info(self, creds):
        sts_client = creds.client('sts')
        response = sts_client.get_caller_identity()

        return response
