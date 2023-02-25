::: mermaid
sequenceDiagram participant imfdatapy participant IMF server

![alt text](https://github.com/sahilmalhotra0510/check/blob/main/mermaid/imfdatapy_architecture_class_diagram/imfdatapy_architecture_class_diagram.PNG?raw=true)
imfdatapy-\>\>IMF server: Meta data request for series IMF
server\--\>\>imfdatapy: JSON imfdatapy-\>\>IMF server: mMta data request
for dimensions IMF server\--\>\>imfdatapy: JSON imfdatapy-\>\>IMF
server: Data request for series IMF server\--\>\>imfdatapy: JSON
:::
