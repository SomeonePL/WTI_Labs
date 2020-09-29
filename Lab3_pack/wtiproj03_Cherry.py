import cherrypy
import json

from wtiproj03_ETL import PMovies # Taki import dziala dzieki __init__.py

def delete():
    pm.fullDrop()
    return {}


@cherrypy.expose
@cherrypy.tools.json_out()
class Ratings(object):
    @cherrypy.tools.accept(media='application/json')
    def GET(self):
        pivoted = pm.getPivotAllTable()
        ret = []

        for index, row in pivoted.iterrows():
            if index < 100:
                ret.append(json.loads(row.to_json(orient='columns')))
            else:
                break

        return ret


@cherrypy.expose
@cherrypy.tools.json_out()
class Rating(object):
    @cherrypy.tools.accept(media="application/json'")
    def POST(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        result = json.loads(rawbody)
        pm.appendRecord(result["userID"], result["rating"], result["movieID"])
        return result


@cherrypy.expose
@cherrypy.tools.json_out()
class Profile(object):
    @cherrypy.tools.accept(media="application/json")
    def GET(self, arg):
        ret = []
        for index, row in pm.getDifferenceWithAvgUser(int(arg)).iterrows():
            ret.append(json.loads(row.to_json(orient="columns")))

        return ret


@cherrypy.expose
@cherrypy.tools.json_out()
class AvgAll(object):
    @cherrypy.tools.accept(media="application/json'")
    def GET(self, args):
        if args == 'all-users':
            ret = []
            for index, row in pm.getAvg().iterrows():
                ret.append(json.loads(row.to_json(orient='columns')))
            return ret[0]
        else:
            ret = []
            for index, row in pm.getPivotUser(int(args)).iterrows():
                ret.append(json.loads(row.to_json(orient='columns')))
            return ret[0]


if __name__ == '__main__':
    pm = PMovies()

    conf = {
        '/':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        'global': {
            'engine.autoreload.on': False
        }
    }

    cherrypy.config.update({'server.socket_port': 6161})
    cherrypy.tree.mount(Ratings(), '/ratings', conf)
    cherrypy.tree.mount(Rating(), "/rating", conf)
    cherrypy.tree.mount(AvgAll(), "/avg-genre-ratings", conf)
    cherrypy.tree.mount(Profile(), "/profile", conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
