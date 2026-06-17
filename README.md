# IEUK Engineering Sector Skills Project

<img src="https://d8qb5cxd9qhkd.cloudfront.net/events/Untitled_design_10_DdDR1D3.jpg"  alt="IEUK 2026">

This project has been set by The Bright Network to be completed for the Internship Experience UK 2026 event

---

## Table of contents

- [Problem Statement](#Problem-Statement)
- [Analysis](#Analysis)
- [Solution](#Solution)

---

## Problem Statement

AeroGrid, a renewal energy provider managing a fleet of offshore wind turbines, has had failures in several of their turbines due to their server being unable to handle all the telemetry data being sent from the turbines. I have been provided 24 hours of turbine telemetry data which I must analyse to identify the failing turbines.
Once the failing machines have been identified, I must design a modern, scalable cloud system which can better handle the constant data being provided by the turbines so this problem can be avoided in the future

---

## Analysis

A turbine requires **urgent maintenance** if:
- Average Temperature exceeds **85 °c**
- Vibration levels spike above **15 mms⁻¹**

From these requirements, I have identified these following outliers

| Turbine ID | Turbine Average Temperature |
|:----------:|:---------------------------:|
| T-04       | 90.6 °c                     |


| Turbine ID | Turbine Average Vibrations |
|:----------:|:--------------------------:|
| T-07       | 20.6 mms⁻¹                 |

I have also produced graphs to show how these turbines differ from the inlier average

![Turbine Temperature over Time](outputs/temperature_outliers.png)

![Turbine Vibrations over Time](outputs/vibration_outliers.png)

---

## Solution

To solve the issuse of the server being unable to handle the large, constant telemetry data from the turbines, I proposed a new data pipeline

```mermaid
graph TD
A[Turbines]
--> B[AWS Kinesis]
--> C[AWS Lamdba]
--> D[Database: New, Averaged Telemetry]
--> E[Database: Old, Outlier Telemetry]
```

Once the data leaves the turbines, it will go the AWS Kinesis where it will be held before
it is processed. It will then go to AWS Lambda where is will be analysed to spot any
outliers. Then it will be delivered to our server to be stored.
To optimise what data is stored on our server, an average of the data for each turbine
could be stored every minute, rather than continuous. After a week or so, the data could
be trimmed to only keep outlying data
