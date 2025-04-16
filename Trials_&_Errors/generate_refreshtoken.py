from google_auth_oauthlib.flow import InstalledAppFlow

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",  # Your downloaded OAuth credentials
        scopes=["https://www.googleapis.com/auth/adwords"]
    )
    credentials = flow.run_local_server(port=8080)
    
    print("Refresh Token:", credentials.refresh_token)

if __name__ == "__main__":
    main()
