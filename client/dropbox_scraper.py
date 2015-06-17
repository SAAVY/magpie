import dropbox
import urllib2

app_key = '0httdxchkqzhydp'
app_secret = 'kzycvt4fb0979qa'


def scrape(url):
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    access_token, user_id = flow.finish(code)

    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()

    # out = open('magnum-opus.txt', 'wb')
    # f, metadata = client.get_file_and_metadata(url)
    # with f:
    #     out.write(f.read())
    # print metadata

if __name__ == "__main__":
    scrape("/s/vzk05zglkqdcqci/mscinotes.pdf")
