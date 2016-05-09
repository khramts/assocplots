from jinja2 import Template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view

def write_to_html(plots, type=0, filename='output.html', title='Title'):
    '''
    Outputs the files into an html file
    :param filename:
    :param labels:
    :param plots:
    :return:
    '''


    # Define our html template for out plots
    template = Template('''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{ title }}</title>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  {{ js_resources }}
  {{ css_resources }}
</head>
<body>

<div class="container-fluid">
  <!-- <div class="jumbotron">
    <h1>Title</h1>
    <p>Description</p>
  </div> --!>
  <h1>{{ title }}</h1>
  <div class="row">
    <div class="col-sm-8">
      <h3>Manhattan plots</h3>
      <p>Group 1</p>
        {{ plot_div.p0 }}
      <p>Group 2</p>
        {{ plot_div.p1 }}
      <p class="text-muted"><a href="https://github.com/khramts/assocplots">Generated with ASSOCPLOTS package</a></p>
    </div>
    <div class="col-sm-4">
      <h3>Quantile-Quantile Plot</h3>
      {{ plot_div.p2 }}
      <p>Selected elements</p>
      {{ plot_div.p3 }}
    </div>
  </div>
</div>

<!-- <footer class="footer">
  <div class="container-fluid">
    <p class="text-muted"><a href="https://github.com/khramts/assocplots">Generated with ASSOCPLOTS package</a></p>
  </div>
</footer> --!>

{{ plot_script }}
</body>
</html>
''')
    resources = INLINE

    js_resources = resources.render_js()
    css_resources = resources.render_css()

    script, div = components({'p0': plots[0],'p1': plots[1],'p2': plots[2],'p3': plots[3]})

    html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       plot_script=script,
                       plot_div=div,
                       title = title)

    with open(filename, 'w') as f:
        f.write(html)

    view(filename)