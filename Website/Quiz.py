import streamlit as st
import numpy as np

from PIL import Image





import streamlit as st
import streamlit.components.v1 as components
components.html("""<div id="foo">hello world!</div>
<img src="data:image/jpeg;base64,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" />
<style>
$('#image').click(function() {
    $('#foo').css({
        'background-color': 'red',
        'color': 'white',
        'font-size': '44px'
    });
});</style>""")
# bootstrap 4 collapse example
components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div id="accordion">
      <div class="card">
        <div class="card-header" id="headingOne">
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
            Collapsible Group Item #1
            </button>
          </h5>
        </div>
        <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #1 content
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header" id="headingTwo">
          <h5 class="mb-0">
            <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
            Collapsible Group Item #2
            </button>
          </h5>
        </div>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
          <div class="card-body">
            Collapsible Group Item #2 content
          </div>
        </div>
      </div>
    </div>
    """,
    height=600,
)