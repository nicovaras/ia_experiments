import subprocess


def _die(msg):
    print msg
    exit(1)


def _parse_xdotool_dimension(text):
    text = text.split('\n')
    position, dimension = text[1].split()[1], text[2].split()[-1]
    left, top = position.split(',')
    width, height = dimension.split('x')
    return map(int, [left, top, width, height])


def get_window_position(name):
    search_window = "xdotool search --onlyvisible --name '^{}'"
    focus_window = "xdotool windowactivate {}"
    window_dimensions = "xdotool getwindowgeometry {}"

    (out, _) = subprocess.Popen(
        search_window.format(name), stdout=subprocess.PIPE, shell=True).communicate()
    if not out or len(out.split()) > 1:
        _die("No se pudo encontrar la ventana")
    window_id = out.strip()

    subprocess.Popen(focus_window.format(window_id), stdout=subprocess.PIPE, shell=True)

    (out, _) = subprocess.Popen(
        window_dimensions.format(window_id), stdout=subprocess.PIPE, shell=True).communicate()
    left, top, width, height = _parse_xdotool_dimension(out)
    return {'width': width, 'height': height, 'left': left, 'top': top}
