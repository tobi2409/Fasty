#zum einmaligen Ausführen

import components.servercomponents.pythonfastapi.builder as builder

builder.build(["components/servercomponents/pythonfastapi/fastapi-main.py",
               "components/servercomponents/pythonfastapi/helloworld.py"], "sample-server.py")