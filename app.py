#!/usr/bin/env python3

import aws_cdk as cdk

from python_cdk_workshop.python_cdk_workshop_stack import PythonCdkWorkshopStack

app = cdk.App()
PythonCdkWorkshopStack(app, "python-cdk-workshop", env=cdk.Environment(region="us-west-2"))

app.synth()
