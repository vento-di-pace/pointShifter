# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pointShifter
                                 A QGIS plugin
 pointShifter
                             -------------------
        begin                : 2016-01-15
        copyright            : (C) 2016 by Eugene Nazarenko
        email                : eugene.v.nazarenko@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load pointShifter class from file pointShifter
    from pointShifter import pointShifter
    return pointShifter(iface)
