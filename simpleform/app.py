import web

urls = (
    '/', 'index',
    '/confirmtweet', 'confirmtweet'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class index(object):
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input(tweet="tweet")
        tweetvar = "%s" % (form.tweet)
        return render.confirmtweet(tweetvar = tweetvar)

class confirmtweet:
    def GET(self):
        tweetvar = "no tweet"
        return render.confirmtweet(tweetvar = tweetvar)

if __name__ == "__main__":
    app.run()
