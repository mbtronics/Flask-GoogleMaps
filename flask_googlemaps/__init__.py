# coding: utf-8

from flask import render_template, Blueprint, Markup, current_app


class Map(object):
    def __init__(self, identifier, lat=None, lng=None,
                 zoom=13, maptype="ROADMAP", markers=None,
                 varname='map',
                 location=None,
                 style="height:300px;width:300px;margin:0;",
                 cls="map", polylines=None, polygons=None,
                 circles=None, rectangles=None, drawing=False):
        self.cls = cls
        self.style = style
        self.varname = varname
        if lat is not None and lng is not None:
            self.center = (lat, lng)
        else:
            self.center = None
        self.location = location or None
        self.zoom = zoom
        self.maptype = maptype
        self.markers = markers or []
        self.identifier = identifier
        self.polylines = polylines or []
        self.polygons = polygons or []
        self.circles = circles or []
        self.rectangles = rectangles or []
        self.drawing = drawing

    def add_rectangle(self, rectangle):
        self.circles.append(rectangle)

    def add_circle(self, circle):
        self.circles.append(circle)

    def add_polygon(self, polygon):
        self.polygons.append(polygon)

    def add_polyline(self, polyline):
        self.polylines.append(polyline)

    def add_marker(self, lat, lng, title="", icon="", info=""):
        self.markers.append({'lat': lat, 'lng': lng, 'title': title, 'icon': icon, 'info': info})

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def js(self):
        return Markup(self.render('googlemaps/gmapjs.html', gmap=self, key=current_app.config['GOOGLEMAPS_KEY']))

    @property
    def html(self):
        return Markup(self.render('googlemaps/gmap.html', gmap=self))


def googlemap_obj(*args, **kwargs):
    map = Map(*args, **kwargs)
    return map


def googlemap(*args, **kwargs):
    map = googlemap_obj(*args, **kwargs)
    return Markup("".join((map.js, map.html)))


def googlemap_html(*args, **kwargs):
    return googlemap_obj(*args, **kwargs).html


def googlemap_js(*args, **kwargs):
    return googlemap_obj(*args, **kwargs).js


class GoogleMaps(object):
    def __init__(self, app=None, **kwargs):
        self.key = kwargs.get('key')
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config['GOOGLEMAPS_KEY'] = self.key if self.key else app.config['GOOGLEMAPS_KEY']
        self.register_blueprint(app)
        app.add_template_filter(googlemap_html)
        app.add_template_filter(googlemap_js)
        app.add_template_global(googlemap_obj)
        app.add_template_filter(googlemap)
        app.add_template_global(googlemap)

    def register_blueprint(self, app):
        module = Blueprint("googlemaps", __name__,
                           template_folder="templates")
        app.register_blueprint(module)
        return module


class PolyLine(object):
    def __init__(self, stroke_color='#FF0000', stroke_opacity=1.0,
                 stroke_weight=2, coordinates=None):
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity
        self.stroke_weight = stroke_weight
        self.coordinates = coordinates or []


class PolyGon(object):
    def __init__(self, stroke_color='#FF0000', stroke_opacity=.8,
                 stroke_weight=2, fill_color='#FF0000',
                 fill_opacity=.35, coordinates=None):
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity
        self.stroke_weight = stroke_weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.coordinates = coordinates or []


class Circle(object):
    def __init__(self, lat, lng, radius=0,
                 stroke_color='#FF0000', stroke_opacity=.8,
                 stroke_weight=2, fill_color='#FF0000', fill_opacity=.35):
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity
        self.stroke_weight = stroke_weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.center = (lat, lng)
        self.radius = radius


class Rectangle(object):
    def __init__(self, left_point, right_point,
                 stroke_color='#FF0000', stroke_opacity=.8,
                 stroke_weight=2, fill_color='#FF0000', fill_opacity=.35):
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity
        self.stroke_weight = stroke_weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.bounds = (left_point, right_point)