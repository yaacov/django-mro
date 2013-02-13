#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2013 Yaacov Zamir <kobi.zamir@gmail.com>
# Author: Yaacov Zamir (2013) <kobi.zamir@gmail.com>

import cairo
import rsvg
import glob
import os

tango_path = './static/tango'
sections = map(os.path.basename, glob.glob('%s/scalable/*' % tango_path))
sizes_array = ['16x16', '22x22', '32x32', '48x48', '150x150', '720x720']

for section in sections:
    print "Rendering section - %s" % section

    svg_files = glob.glob('%s/scalable/%s/*.svg' % (tango_path, section))

    for svg_file_name in svg_files:
        base = os.path.basename(svg_file_name)
        print " file - %s" % base

        png_file_name = os.path.splitext(base)[0]

        svg = rsvg.Handle(svg_file_name)
        svg_w, svg_h = svg.props.width, svg.props.height

        for size in sizes_array:
            png_w, png_h = map(int, size.split('x'))

            img = cairo.ImageSurface(cairo.FORMAT_ARGB32, png_w, png_h )
            ctx = cairo.Context(img)
            w_ratio, h_ratio = float(png_w) / float(svg_w), float(png_h) / float(svg_h)
            ratio = min(w_ratio, h_ratio)

            ctx.scale(ratio, ratio)
            ctx.translate(100,0)
            ctx.scale(1.1, 1.1)

            svg.render_cairo(ctx)

            png_dir = '%s/%s/%s' % (tango_path, size, section)
            try:
                os.makedirs(png_dir)
            except:
                pass
            img.write_to_png('%s/%s.png' % (png_dir, png_file_name))
