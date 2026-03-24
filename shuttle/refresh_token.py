from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

    # Run local server on a safe port
    creds = flow.run_local_server(port=0)  # '0' lets OS pick an open port

    print("REFRESH TOKEN:", creds.refresh_token)
    # Optionally save it to a file
    with open("gmail_refresh_token.txt", "w") as f:
        f.write(creds.refresh_token)


if __name__ == "__main__":
    main()