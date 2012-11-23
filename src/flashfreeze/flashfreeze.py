from ghost import Ghost
import sys
import time

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <url>\n" % (argv[0],))
        return 1

    ghost = Ghost(viewport_size=(1280, 1024))
    # ghost = Ghost(viewport_size=(1280, 1024), display=True)
    # ghost.webview.getSettings().setPluginsEnabled(true);
    page, resources = ghost.open(argv[1])
    #assert page.http_status==200 and 'bbc' in ghost.content
    time.sleep(10)
    ghost.capture_to('screenshot2.png')
    ghost.exit()

    for r in resources:
      print "R:",r.url

if __name__ == "__main__":
    sys.exit(main(sys.argv))
