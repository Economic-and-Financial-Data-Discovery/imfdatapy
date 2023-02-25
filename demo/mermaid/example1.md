<div class="mermaid">

sequenceDiagram participant imfdatapy participant IMF server
imfdatapy-\>\>IMF server: Meta data request for series IMF
server--\>\>imfdatapy: JSON imfdatapy-\>\>IMF server: mMta data request
for dimensions IMF server--\>\>imfdatapy: JSON imfdatapy-\>\>IMF server:
Data request for series IMF server--\>\>imfdatapy: JSON

</div>
