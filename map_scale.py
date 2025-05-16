def calculate_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()
    
    width = abs(float(upper_corner[0]) - float(lower_corner[0]))
    height = abs(float(upper_corner[1]) - float(lower_corner[1]))
    
    return f"{width},{height}"
