---
title: "Leveraging Azure Application Insights with OpenTelemetry: Distributed Tracing Done Right"
date: 2025-03-13T13:17:36+0000
lastmod: 2025-03-17T13:35:30+0000
slug: "leveraging-azure-application-insights-with-opentelemetry-distributed-tracing-done-right"
summary: "Learn about migrating .NET applications to Azure's OpenTelemetry-based Application Insights for seamless distributed tracing, simplified observability, and minimal code impact."
tags: ["azure", "cloud", "csharp", "observability", "opentelemetry"]
feature_image: "https://images.unsplash.com/photo-1613228489368-75c0bad290ff?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDN8fG9ic2VydmV8ZW58MHx8fHwxNzQxODcxNzcxfDA&ixlib=rb-4.0.3&q=80&w=2000"
aliases:
  - /leveraging-azure-application-insights-with-opentelemetry-distributed-tracing-done-right/
---

**Summary:**  
Azure Application Insights has long supported distributed tracing, but its recent migration to Open Telemetry takes observability to a new level. For applications using older Application Insights SDKs, migrating to the modern `Azure.Monitor.OpenTelemetry.AspNetCore` library provides seamless integration with minimal code changes, unlocking vendor-neutral observability and richer telemetry capabilities. This article covers the architectural patterns, migration strategies, and practical examples for developers and architects, highlighting the simplicity of ILogger integration, cross-platform support, and unified data analysis via Log Analytics. Whether running .NET apps, Azure Databricks jobs, or other services, leveraging Azure’s Open Telemetry distribution ensures consistent, comprehensive, and scalable observability across your Azure solutions.

We'll cover some architectural discussion on how Azure Application Insights supports distributed tracing, its migration to Open Telemetry, and how it integrates with .NET applications and when needed even Azure Databricks.

## Overview of Distributed Tracing in Azure Application Insights

Azure Application Insights (AI) provides **distributed tracing** to follow a transaction across different services. Originally, Application Insights SDKs handled tracing by generating a unique operation ID for each request and propagating it via HTTP headers like `Request-Id` and `Request-Context`. This allowed linking telemetry from separate components – for example, a front-end web app and a back-end API – even if they reported to different AI instances ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=Image%3A%20%2Fmedia%2F2019%2F10%2Fcarbonpaper)). The front-end would include its AI **App ID** in the outbound call headers, and the back-end would respond with its own App ID. Application Insights used these IDs to stitch together a single end-to-end trace in the portal, showing the relationship between requests and dependencies across components ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=It%20does%20this%20by%20having,the%20calling%20Application%20Insights%20instance)). This **proprietary correlation protocol** worked, but it was tied to AI-specific headers (`Request-Id`, `Request-Context`) and required all components to use Application Insights SDKs.

Over time, the industry moved toward standardizing distributed tracing. Azure Application Insights began transitioning to the **W3C Trace Context** standard, which defines `traceparent` and `tracestate` headers for vendor-neutral trace propagation. Modern AI SDKs support W3C Trace Context (with backward compatibility to the old Request-Id system). In parallel, the industry converged on **OpenTelemetry (OTel)** – an open-source CNCF project formed by merging OpenTracing and OpenCensus in 2019. OpenTelemetry provides standard APIs for traces, metrics, and logs, solving the lack of cross-platform standards in observability.

## **Transition to Open Telemetry**

Azure Monitor (which underpins Application Insights) is adopting Open Telemetry as the instrumentation layer. Microsoft’s Azure Monitor Open Telemetry **Distro** is essentially a supported wrapper around the standard OTEL SDKs. The move brings several benefits:

- **Vendor Neutrality & Ecosystem:** OpenTelemetry is vendor-neutral and widely supported. By embracing OTel, Application Insights can ingest telemetry from any language or platform that supports OTel, beyond the languages originally supported by the AI SDKs. This opens up integration with open-source tools and APM systems (e.g. Prometheus, Jaeger, Zipkin, Grafana) in addition to Azure’s own monitoring ([Introducing Azure Monitor OpenTelemetry Distro - InfoQ](https://www.infoq.com/news/2023/06/azure-opentelemtry-distro/#:~:text=Microsoft%20Azure%20uses%20OpenTelemetry%20technology,native%20monitoring%20solution%2C%20Azure%20Monitor)).
- **Standardization:** Using OTel means Azure uses industry-standard trace context. This eases end-to-end tracing across components using different tech stacks or third-party libraries, since they can all speak the same telemetry language. It also aligns Azure with evolving standards, avoiding vendor lock-in for customers ([OpenTelemetry help and support for Azure Monitor Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-help-support-feedback#why-should-i-use-the-azure-monitor-opentelemetry-distro#:~:text=instrumentation%20libraries.%20,to%20%2011%20embrace%20open)).
- **Performance and Features:** The OpenTelemetry SDKs are designed for high performance at scale and offer a rich set of instrumentation libraries. Microsoft notes that OTel SDKs tend to be more performant than the older AI SDKs in high-scale scenarios ([OpenTelemetry help and support for Azure Monitor Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-help-support-feedback#why-should-i-use-the-azure-monitor-opentelemetry-distro#:~:text=instrumentation%20libraries.%20,to%20%2011%20embrace%20open)). Additionally, OTel enables collection of new telemetry types (e.g. more granular metrics, logs) that were not originally in the AI SDK scope.
- **Community and Adoption:** OpenTelemetry has strong community momentum. It’s a CNCF incubating project with broad industry contribution (over 1,000 contributors from companies like Google, Microsoft, Amazon, Splunk, etc.). It is fast becoming the *de facto* standard for observability across cloud and application platforms.

By migrating to OpenTelemetry, Application Insights essentially becomes a backend for standard OTel data. The **trace collection** is now open-standard: any OTel-compatible tracer can send distributed traces to AI. This transition preserves AI’s powerful analysis capabilities while making instrumentation more flexible. In summary, Application Insights started with its own tracing mechanism and has evolved to adopt OpenTelemetry for a more open, interoperable, and future-proof distributed tracing solution ([Introducing Azure Monitor OpenTelemetry Distro - InfoQ](https://www.infoq.com/news/2023/06/azure-opentelemtry-distro/#:~:text=Microsoft%20Azure%20uses%20OpenTelemetry%20technology,native%20monitoring%20solution%2C%20Azure%20Monitor)).

### **Industry References**

Open Telemetry’s origins as a merger of Open Tracing and Open Census in 2019 under CNCF highlight the industry’s push for a unified standard. Today, all major cloud vendors and APM providers have embraced OTel. Azure’s adoption of OpenTelemetry (including creating the Azure Monitor OpenTelemetry Distro) is a concrete example of this industry trend ([Introducing Azure Monitor OpenTelemetry Distro - InfoQ](https://www.infoq.com/news/2023/06/azure-opentelemtry-distro/#:~:text=Microsoft%20Azure%20uses%20OpenTelemetry%20technology,native%20monitoring%20solution%2C%20Azure%20Monitor)). It demonstrates how cloud platforms are aligning with open-source standards to improve integration and reduce the burden of instrumenting distributed systems.

## Application Architecture Using Application Insights

Integrating Application Insights into a distributed application can be done in a couple of patterns. The goal is to capture telemetry (logs, traces, metrics) from all components of the system in a way that you can easily diagnose issues across service boundaries. Key design choices include whether to use a **separate Application Insights instance per component** or a **shared instance for multiple components**, and how to leverage **Log Analytics** for centralized data analysis.

### **Separate vs. Shared Application Insights Instances**

In a microservices or multi-tier architecture, one option is to give each application or service its own AI resource (separate instances). Another option is to have multiple services report into a single, shared AI resource. Each approach has pros and cons:

- *Separate AI per service:* This isolates telemetry by service. Each service’s data (requests, logs, dependencies, exceptions) goes to its own Application Insights instance. This can be useful for ownership (each team manages their AI), differing retention settings, or reducing noise between unrelated components. With separate instances, distributed tracing still works across them by using correlation IDs and the Application Map can link the services via their **Cloud role names and App IDs** ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=Image%3A%20%2Fmedia%2F2019%2F10%2Fcarbonpaper)) ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=It%20does%20this%20by%20having,the%20calling%20Application%20Insights%20instance)). However, querying end-to-end transactions requires joining data from multiple AI resources (the Azure portal’s “end-to-end transaction” view or cross-resource Log Analytics queries).
- *Shared AI for multiple services:* In this model, multiple components (e.g. a front-end and a back-end) send telemetry to the **same** Application Insights resource. This makes it very easy to see all telemetry in one place and do holistic queries – since all logs and spans share one store. Application Insights distinguishes the services by **cloud role name** (a property on each telemetry item indicating the service or role that generated it). For example, you might set `cloud_RoleName = "frontend-web"` and `cloud_RoleName = "orders-api"` for different components. The SDKs (both classic and OTel-based) will often set a default role name (like the Azure service name or assembly name) which you can override via configuration or TelemetryInitializers. Using one AI resource means the **Application Map** (which shows a topology of services) is built automatically using cloud role names, without needing to configure External App ID linkage. The downside could be potential performance or data volume limits on a single AI resource if many services push data, and lack of isolation (all teams with access see all telemetry).

In practice, a **multi-component application** can be monitored either way. Microsoft now leans toward using a single **workspace-based** Application Insights for related components, because Log Analytics can segregate or filter by role name easily, while providing a unified query surface. If separate AI instances are used, you can still **link them**: historically, the `Request-Context` header with `appId` was used to tie together separate AI instances in a trace ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=It%20does%20this%20by%20having,the%20calling%20Application%20Insights%20instance)). Today, with OpenTelemetry and W3C tracecontext, as long as trace IDs are propagated, the distributed trace will exist; but to view it end-to-end in the Azure portal, the telemetry from each service needs to be in the same workspace or linked via the Application Map (which still uses the concept of App ID or connected AI resources).

## **Role of Log Analytics**

Log Analytics acts as the **central storage and analysis layer** for Azure Monitor telemetry. In newer Application Insights (workspace-based), each AI resource is backed by an Azure Monitor Log Analytics workspace. All telemetry – whether it’s incoming request traces, application logs, exceptions, or custom metrics – is stored as records in that workspace (in tables like `AppTraces`, `AppRequests`, etc.). This means you can use Kusto Query Language (KQL) in Log Analytics to query and join across all data types. It also means multiple Application Insights resources can write to the *same* Log Analytics workspace, consolidating data. For example, you might have separate AI instances for `frontend` and `backend` apps, but both send their data to a single Log Analytics workspace. You can then run a single query to see combined logs or correlated operation IDs across both. Azure Monitor’s design encourages using Log Analytics as the unified data layer: “**Logs**: Retrieve, consolidate, and analyze all data collected into Azure Monitor Logs” ([Application Insights OpenTelemetry overview - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview#:~:text=,that%20visualize%20application%20monitoring%20data)). Whether using separate or shared AI resources, if they share a workspace or you utilize cross-resource queries, Log Analytics allows SREs and developers to get a holistic view.

Below are diagrams illustrating two architectural approaches:

### **Separate Application Insights per Service**

In this approach, each microservice or application has its own Application Insights instance. The distributed tracing correlation is achieved via operation IDs and App ID exchange between services. Telemetry for each service is siloed in its respective AI resource, but you can enable the Application Insights **Application Map** to visualize the connections (it uses the cloud role name or App ID to link the nodes). All telemetry ultimately lands in Log Analytics (either each AI has its own workspace or they all send to one workspace).

```

flowchart LR
    subgraph Client
        User
    end
    subgraph Services
        Frontend["Frontend Service"] -->|HTTP call| Backend["Backend Service"]
    end
    User -->|request| Frontend
    Backend -->|response| Frontend -->|response| User
    Frontend == "Telemetry" ==> AI_Front[(App Insights - Frontend)]
    Backend == "Telemetry" ==> AI_Back[(App Insights - Backend)]
    subgraph Azure_Monitor["Azure Monitor / Log Analytics"]
        AI_Front --> LogW[(Log Analytics Workspace)]
        AI_Back --> LogW
    end
    style AI_Front fill:#FFD,stroke:#333,stroke-width:1px;
    style AI_Back fill:#FFD,stroke:#333,stroke-width:1px;
    style LogW fill:#E6F5E1,stroke:#333,stroke-width:1px;

```

*Diagram: Two services (frontend and backend) use separate Application Insights. Correlation is done via trace context (the frontend passes a trace ID and its AI App ID to the backend). Telemetry from each goes to its own AI resource, which are connected in the Application Map. Both AI resources can send data to a single Log Analytics workspace for unified querying.*

In the above scenario, the **frontend** and **backend** each have distinct instrumentation keys (or connection strings). When the frontend calls the backend, the AI SDK (or OTel instrumentation) adds a header like `Request-Context: appId=<Frontend_AppId>` and a `traceparent` with the operation ID ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=It%20does%20this%20by%20having,the%20calling%20Application%20Insights%20instance)). The backend’s instrumentation picks that up, knows the call came from an external component, and includes the caller’s appId in its telemetry (in the `dependency.target` or `request.source` fields) ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=It%20does%20this%20by%20having,the%20calling%20Application%20Insights%20instance)) ([Things I wish I knew earlier about Distributed Tracing in Azure Application Insights - Brett McKenzie](https://brettmckenzie.net/posts/things-i-wish-i-knew-earlier-about-distributed-tracing-in-azure-application-insights/#:~:text=Image%3A%20%2Fmedia%2F2019%2F10%2Fresponse)). In Application Insights, this appears as a linked request and dependency. We get a distributed trace that spans both AI instances. In Log Analytics, you could query by the operation ID (which is shared) to get combined data. Each AI resource can be managed independently (different alert rules, permissions, retention), which is useful if, say, the backend is a shared service used by multiple frontends.

### **Shared Application Insights for Multiple Applications**

In this approach, multiple services report into one Application Insights instance. For example, an Azure Function and an App Service may use the same AI resource. Telemetry is distinguished by a role name or instance name. The advantage is simplicity: a single place to search all telemetry, and built-in correlation since everything shares one instrumentation key.

```

flowchart LR
    subgraph Services
        ServiceA["Service A"] -->|calls| ServiceB["Service B"]
    end
    ServiceA == "Telemetry" ==> AI_Shared[(Application Insights)]
    ServiceB == "Telemetry" ==> AI_Shared
    AI_Shared --> LogWS[(Log Analytics Workspace)]
    style AI_Shared fill:#FFD,stroke:#333,stroke-width:1px;
    style LogWS fill:#E6F5E1,stroke:#333,stroke-width:1px;

```

*Diagram: Two services use a single, shared Application Insights resource. The AI resource tags data with each service’s **cloud\_RoleName** to differentiate them. All telemetry is stored together in one Log Analytics workspace.*

In this setup, you might configure each service’s telemetry initializer (or via OTel Resource configuration) to set a unique `cloud_RoleName`. For instance, **Service A** might appear as “frontend-web” and **Service B** as “orders-api” in the data. Application Insights automatically populates `cloud_RoleInstance` (e.g. machine or host name) and `cloud_RoleName` for many Azure services, or you can set it manually. The Application Map in the portal will group telemetry by role name, showing the two services as separate nodes even though they share one AI resource. Searching logs or using Analytics is straightforward since all records are in one place – you can simply filter by `cloud_RoleName` to separate concerns. One thing to watch is volume and access control: all teams pushing to a shared AI need coordinated access. Also, if one service generates a huge volume of telemetry, it could impact the ingestion volume of the shared AI (hitting caps or making it harder to manage retention for just one service).

**Log Analytics as the Analysis Layer:** In both patterns, Log Analytics is crucial. It provides a query engine to slice and dice telemetry. If using **workspace-based** Application Insights, each AI instance is tied to a workspace – potentially the same one – making cross-service queries seamless. If using classic AI (non-workspace-based), each AI has its own store, but you can use Azure Monitor **Cross-resource queries** (using the `app("AI Resource Name").requests` syntax in KQL) to query across resources. Log Analytics also enables creating **workbooks** and dashboards that pull in data from multiple sources (for example, combining metrics from App Insights and Azure platform logs). Many Azure Monitor features, like alerts and workbooks, ultimately run queries against Log Analytics, reinforcing its role as the unified data layer.

In summary, **architectural integration patterns** for Application Insights can vary, but leveraging cloud role names and Log Analytics allows flexibility. A typical enterprise might use *one AI instance per microservice* during development (for isolation), but in production, consolidate telemetry into fewer instances or a single workspace for a holistic view. The choice often comes down to how tightly coupled the services are, who needs access to the data, and organizational preferences on tenancy.

## Migration from Application Insights SDK to `Azure.Monitor.OpenTelemetry.AspNetCore`

Application Insights’ **classic SDK for .NET** (e.g. `Microsoft.ApplicationInsights.AspNetCore` and related packages) provided automatic instrumentation and a `TelemetryClient` API for custom telemetry. While functional, the classic SDK had some limitations: it was a proprietary implementation, required separate SDKs per language, and had a fixed set of features that evolved slowly. For instance, developers often had to explicitly initialize the SDK (calling `AddApplicationInsightsTelemetry()` in ASP.NET Core or setting up configuration files in .NET Framework), and use `TelemetryClient` to track custom events or dependencies. Extending it (beyond what was automatically collected) meant learning AI-specific concepts like Telemetry Initializers, Telemetry Processors, and the old correlation headers. There were also quirks – e.g., **ILogger** and AI’s `TelemetryClient` could both send logs, sometimes leading to duplicate or uncorrelated entries if not configured carefully.

The migration to `Azure.Monitor.OpenTelemetry.AspNetCore` represents a shift to the OpenTelemetry-based pipeline for .NET applications. This **Azure Monitor OpenTelemetry Distro** (distribution) encapsulates the OTel SDK with presets for Azure. The new package addresses many of the old SDK’s limitations:

- **Unified Telemetry Model:** Instead of separate mechanisms for traces, logs, and metrics, OpenTelemetry offers all three signals in one framework. The Azure Monitor distro configures an OTel **TracerProvider** for distributed traces (requests, dependencies), a **MeterProvider** for metrics, and a **LoggerProvider** for logs – all wired to Azure Monitor export. This unified model simplifies configuration and reduces the need for separate SDKs or manual correlation. Essentially, one instrumentation pipeline handles everything.
- **Ease of Setup:** With the classic SDK, you had to install and configure multiple pieces (SDK, instrumentation key, possibly enable W3C, etc.). The new approach significantly simplifies this. In an ASP.NET Core app, you typically just install the NuGet package `Azure.Monitor.OpenTelemetry.AspNetCore` and add one line in your startup: `builder.Services.AddOpenTelemetry().UseAzureMonitor()` ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=To%20enable%20Azure%20Monitor%20Distro%2C,from%20your%20Application%20Insights%20resource)). This single call replaces `AddApplicationInsightsTelemetry()` and automatically registers all the instrumentations (for incoming HTTP, outgoing HTTP, SQL calls, etc.) that you’d get from AI, plus sets up log and metric collection. The connection string for your AI resource can be provided via code or environment (`APPLICATIONINSIGHTS_CONNECTION_STRING`) ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=To%20enable%20Azure%20Monitor%20Distro%2C,from%20your%20Application%20Insights%20resource)). For many applications, migration is as simple as removing the old AI SDK package and adding the new one with minimal code changes ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=To%20enable%20Azure%20Monitor%20Distro%2C,from%20your%20Application%20Insights%20resource)).
- **Feature Parity and Improvements:** The Azure Monitor OTel distro is designed to provide a similar experience to the AI SDK. It includes support for **automatic dependency tracking**, live metrics, sampling, etc., so you shouldn’t lose major functionality by migrating. In fact, some capabilities are improved:
  - It uses the W3C TraceContext by default for correlation (no need for manual opt-in).
  - It includes additional instrumentation (e.g., out-of-the-box support for SQL client, gRPC, etc. via OTel instrumentation libraries) which might not have been available or as robust in the old SDK ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=builder.Services.AddOpenTelemetry%28%29.UseAzureMonitor%28%29%3B%20builder.Services.ConfigureOpenTelemetryTracerProvider%28%28sp%2C%20builder%29%20%3D)).
  - Performance is likely better under load, thanks to the efficiency of the OTel SDK ([OpenTelemetry help and support for Azure Monitor Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-help-support-feedback#why-should-i-use-the-azure-monitor-opentelemetry-distro#:~:text=instrumentation%20libraries.%20,to%20%2011%20embrace%20open)).
  - The distro also brings **Azure-specific enhancements** on top of OTel, like offline storage for transient network issues, Azure AD authentication support (for sending telemetry without instrumentation key), and automatic population of Azure resource attributes (cloud role) – features that were in the classic SDK and preserved or reimplemented in the new pipeline.
- **Limitations of the old vs new:** One limitation of the older AI SDK was that it was not **vendor-neutral** – if you ever wanted to send telemetry to a system other than Application Insights, you’d need a completely different SDK. With OpenTelemetry, you have the option to swap out the exporter (for example, send to Jaeger or Zipkin for testing) without changing your instrumentation code. This decoupling can be seen as future-proofing your observability. The new Azure Monitor exporter specifically sends data to Application Insights, but because it’s using standard OTel, you could also collect the same telemetry to other sinks if needed with minor tweaks.

**Migration Steps & Complexity:** Migrating an ASP.NET Core application typically involves:

1. **Remove the old SDK** – e.g. uninstall `Microsoft.ApplicationInsights.AspNetCore` NuGet and any related AI packages. Also remove any `.UseApplicationInsights()` or `AddApplicationInsightsTelemetry()` calls in your code, and delete AI config files if present.
2. **Install the Azure Monitor OpenTelemetry Distro** – add the NuGet package `Azure.Monitor.OpenTelemetry.AspNetCore` (latest version 1.x).
3. **Configure as needed** – You can customize the setup via OpenTelemetry APIs if necessary. For example, if you need additional instrumentation (like gRPC client, or a custom ActivitySource), you can use `builder.Services.ConfigureOpenTelemetryTracerProvider(...)` to add sources or instrumentations after calling `UseAzureMonitor()` ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=match%20at%20L253%20builder,builder.AddGrpcClientInstrumentation)). The distro is designed to cover most common needs without extra code, but it’s extensible. You might also adjust logging filters or add processors (e.g., to redact sensitive data – which can be done via OTel processors or config, as shown in Microsoft docs).
4. **Test and validate** – After migration, you should run and ensure that requests, dependencies, exceptions, and custom logs appear in Application Insights as before. The telemetry types may have slight name changes (for instance, AI “Trace” telemetry corresponds to OTel logs). It’s good to verify that the **distributed trace correlation** still works (it should, as OTel uses the same trace IDs but ensure any custom dependency tracking is updated to use OTel APIs if needed).

**Enable OTel instrumentation** – in your `Program.cs` or Startup, add the OTel initialization. For example:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenTelemetry().UseAzureMonitor(o => 
{
    o.ConnectionString = "<Your AI Connection String>";
    // o.SamplingRatio = 1.0; // (optional) adjust sampling if needed
});
// ...other services like controllers
var app = builder.Build();
app.Run();

```

This single call sets up the **TracerProvider**, **MeterProvider**, and **LoggerProvider** under the hood. By default, it will instrument ASP.NET Core requests and dependencies. If you had custom telemetry (like TrackEvent calls), you’ll handle those differently (more on that below).

The level of complexity in migration is moderate. For straightforward web apps that mainly relied on automatic monitoring, it’s largely a drop-in replacement with minimal code changes. The Azure docs indicate you can expect a similar experience after migration. However, if you had deep customization (custom telemetry initializers, extensive use of `TelemetryClient` for manual events, etc.), you’ll need to replace those with OpenTelemetry equivalents. For example:

- Replacing `TelemetryClient.TrackTrace("message", SeverityLevel.Information)` with using **ILogger** logging (which will be captured by OTel as logs).
- Replacing `TelemetryClient.StartOperation<RequestTelemetry>("opName")` with either using the ASP.NET Core request automatically, or creating a manual `Activity` via OTel’s API (though most web frameworks auto-generate an Activity for requests).
- Custom metrics via `TrackMetric` might be replaced by OTel Meter API usage (or writing to Azure Monitor Metrics via other means).

**Automatic instrumentation vs. manual:** The new OTel SDK with Azure Monitor provides **automatic instrumentation** for a lot of common scenarios – HTTP, SQL, Azure SDK calls, etc., similar to the old SDK. If you need to instrument custom operations, you’d use OpenTelemetry’s API (e.g., `ActivitySource.StartActivity` in .NET to create custom spans). The Azure distro includes an ActivitySource named `Microsoft.AspNetCore.Hosting` for incoming requests, among others. It also captures exceptions and logs automatically. Configuration can be done via code or via `appsettings.json`/environment variables as shown in docs (for example, you can set `AzureMonitor.ConnectionString` in config instead of code, and it will be picked up).

**Summary of Benefits:** By moving to `Azure.Monitor.OpenTelemetry.AspNetCore`, you benefit from being in line with the industry-standard approach. You reduce dependency on proprietary SDKs and gain access to the broader OTel ecosystem (which means easier instrumentation of libraries and the ability to direct telemetry elsewhere if needed). Microsoft will also likely add new features to the OTel pipeline first. Given that Microsoft’s own reasoning is that OTel SDKs are more performant and flexible ([OpenTelemetry help and support for Azure Monitor Application Insights - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-help-support-feedback#why-should-i-use-the-azure-monitor-opentelemetry-distro#:~:text=instrumentation%20libraries.%20,to%20%2011%20embrace%20open)), adopting this should improve the telemetry pipeline’s efficiency. Additionally, the **maintenance burden** shifts – you no longer worry about the intricacies of the AI SDK internals, and instead configure standard OTel components (for which a lot of community knowledge exists). The migration is designed to be as smooth as possible, with Microsoft providing documentation and a mapping of features from the old API to the new one. Most developers report only minor changes were needed in application code, mostly around how they log or track custom events.

## Separation of Logging and Tracing in .NET Applications

In .NET, the `ILogger` abstraction (from Microsoft.Extensions.Logging) is commonly used for **logging** within applications. It provides methods like `LogInformation`, `LogWarning`, etc., and it’s indifferent to the logging backend – it could be console, file, Application Insights, etc. When it comes to Application Insights and OpenTelemetry, it’s important to understand how logging (via ILogger) and distributed tracing relate, and how a developer’s experience changes (or doesn’t) when migrating to the new system.

**ILogger and Application Insights:** In the classic Application Insights SDK, an `ILogger` could be configured to send logs to AI by adding the `ApplicationInsightsLoggerProvider`. This meant every `ILogger.LogX` call became a “Trace” telemetry in Application Insights (with severity mapping to AI’s Trace severity). Under the hood, `ApplicationInsightsLoggerProvider` would use the same TelemetryChannel as other AI telemetry, ensuring your logs went to the same place as your requests and dependencies. Many developers got used to just writing `ILogger` logs in their ASP.NET Core apps and having them show up in the AI portal under the **Traces** table or Search.

With OpenTelemetry, the idea is similar: **logging is integrated via ILogger**. The Azure Monitor OpenTelemetry Distro includes an **OpenTelemetry Logging** component that listens to `ILogger` providers. In fact, the distro automatically captures logs created with `Microsoft.Extensions.Logging` (which is what ILogger is). For the developer, this means you **continue to use ILogger as before** – you do not need to call a special AI API to log things. When you switch to the OTel-based SDK, you might remove the old `builder.Logging.AddApplicationInsights()` line (that registered the old provider), but the new `UseAzureMonitor()` will internally register an OTel logger provider that hooks into the ILogger pipeline. All your existing `LogInformation`, `LogError`, etc. calls will be captured by OpenTelemetry and exported to Azure Monitor as log records.

**Logs vs. Traces (Distributed Traces):** It’s important to clarify terminology: In Application Insights, a “Trace” usually referred to a log message (text log). But in distributed tracing context, a “Trace” is a sequence of spans (operations) across services. OpenTelemetry uses the term *Log* to mean log messages, and *Trace* to mean the distributed trace. To avoid confusion, consider “Application Insights trace telemetry” = log entries. In the new world, your ILogger logs become OTel LogRecords which are sent to Azure Monitor – they’ll still appear in the “traces” table in Log Analytics (since that’s historically where AI stores log messages). The **distributed trace spans** (requests, dependencies, etc.) are handled by the OTel Tracer and show up in AI as requests/dependencies with correlation.

For developers, **tracing** (the distributed kind) is often implicit. For example, when a web request comes in, the instrumentation automatically starts an Activity (span) and tracks the incoming request and outgoing calls. Developers typically didn’t manually create spans in the AI SDK (except for custom scenarios where they might use `TelemetryClient.StartOperation`). In .NET, the `System.Diagnostics.Activity` class is the core of tracing – and OTel builds on that. With the OpenTelemetry SDK, if a dev does nothing special, they still get distributed traces: the HTTP libraries create Activity objects for outgoing requests, ASP.NET Core instrumentation creates one for the inbound request, etc. These get recorded and sent. If a developer *wants* to add custom spans, they would now use the OpenTelemetry API or `ActivitySource` to do so, rather than AI’s TelemetryClient. This is a shift in approach but aligns with the .NET platform’s direction (System.Diagnostics is built-in, whereas TelemetryClient was external).

**Impact on Software Developers (Switching to OTel):** For most developers, switching to the OpenTelemetry-based implementation has minimal impact on how they write logging and tracing code:

- **Logging:** Continue to use `ILogger<T>` in ASP.NET Core or .NET apps. No changes needed in most cases. The categories, event IDs, and log levels all flow through. One current gap is that **ILogger scopes** (the logical operation scopes you can create in logging) might not automatically flow to AI as custom dimensions unless configured, which is a difference to note (there’s ongoing work in the OTel .NET community to handle scopes). But message and severity all go through. Developers do not have to learn a new logging API – `ILogger` remains the abstraction for generating logs, and the telemetry pipeline (now OTel) takes care of exporting them.
- **Tracing:** Most tracing is automatic. Developers should be aware that **correlation still happens**, but via Activity context. For example, if you log something via ILogger inside an HTTP request, Application Insights will still correlate that log with the request via the trace ID. This is because under the hood, the OTel logger provider attaches trace context (Activity current) to the logs. In AI, you’ll see the logs associated with the appropriate operation ID. From a code perspective, you don’t have to manually do anything for this correlation (same as with the old SDK, where it also did correlation automatically). The recommendation is to avoid using `TelemetryClient` in new code – instead, if you want to track a custom event or trace, either use ILogger for simple logs or use Activity/OTel APIs for more complex custom spans.
- **Custom Telemetry API:** If you used `TelemetryClient.TrackEvent`, `TrackException`, etc., those specific APIs are not part of OpenTelemetry. The alternatives are:
  - Exceptions: just throw them or log them; the OTel instrumentation will capture unhandled exceptions and send them as error telemetry. Or use `ILogger.LogError(ex, "...")` which will record an exception.
  - Events: OTel doesn’t have “custom events” in the same way. Often, a custom event can be modeled as a log (e.g., an ILogger LogInformation with a specific category or structured state) or as a span with an event attribute. You might create an Activity for a business operation and add attributes denoting what happened.
  - Metrics: use OpenTelemetry Metrics API (Meter, Counter, etc.) to create custom metrics which are exported to Azure Monitor.

So developers may need to refactor those usages. But importantly, these changes push developers toward using **framework-neutral APIs** (ILogger, Activity, OTel API) instead of Application Insights-specific ones. This decouples application code from the telemetry backend. For example, a developer can instrument an Activity for a custom operation; if later the company switches telemetry backend, that code is still standard OTel and will work.

**ILogger Abstraction:** `ILogger` itself doesn’t know about traces vs. metrics – it’s purely for logs. But the presence of `Activity.Current` when logging ties the log to a trace. In practice, after migration, developers might notice that the **category name** of the ILogger (usually the fully qualified class name) appears differently or is missing in AI. There have been some reports that OTel logging initially did not include the logger category as a property in AI (unlike the old provider which included a SourceContext). This is a minor schema difference that could impact how you filter logs. The OpenTelemetry team has been addressing such gaps. For example, making the `ILogger` category available via a property (like `LogCategory`) in the exported data is on the roadmap. For now, developers might add the category name as part of the log message or use scopes if needed for filtering.

In summary, **logging and tracing are now more separated conceptually but unified under OpenTelemetry’s umbrella**. You log with ILogger (goes to logs pipeline), you let the automatic instrumentation handle tracing (or use ActivitySource for custom spans). The benefit is that as a developer, you mostly continue with the same patterns – using DI to get `ILogger<T>` for logging and relying on the framework to handle request and dependency tracking. The heavy lifting of correlating logs with traces is handled by the telemetry system, just as before. So the impact of switching to the OpenTelemetry-based AI is largely *under the hood*. You’ll spend less time dealing with Application Insights SDK specifics (like no more TelemetryInitializer classes to set role name – OTel resource does it, etc.), and more time with either standard .NET features or configuration. For an engineer, this feels more natural as part of the .NET ecosystem rather than a bolt-on.

## Integration with Azure Databricks and Other Azure Services

Application Insights isn’t just for .NET or web apps – you can use it to gather telemetry from data and compute platforms like **Azure Databricks**, as well as functions, containers, etc. With the move to OpenTelemetry, Microsoft provides new options to integrate these services. Let’s focus on **Azure Databricks**, which often involves **Spark jobs in Python or Scala**, and discuss how to send logs/metrics/traces to Application Insights. We’ll also touch on deciding between separate or shared AI instances in such scenarios, and mention other services briefly.

**Azure Databricks (Python) with Azure Monitor OpenTelemetry:** Azure Databricks is a Spark-based analytics platform, and you can run custom code (PySpark, Scala, .NET Spark). To instrument Databricks workloads and send telemetry to Application Insights, you can leverage the **OpenTelemetry SDK for Python** along with the Azure Monitor exporter. Microsoft provides the `azure-monitor-opentelemetry` package (Azure Monitor OpenTelemetry Distro for Python) to streamline this integration. This package acts as a one-stop solution: it bundles the OpenTelemetry Python SDK, some common instrumentation libraries, and the Azure Monitor exporter. Using it in Databricks typically involves:

1. **Install the package** in your Databricks environment (e.g., via `%pip install azure-monitor-opentelemetry` in a notebook or as a cluster library). It requires Python 3.8+ which Databricks supports.
2. **Automatic instrumentation in Databricks:** The Python distro will automatically instrument HTTP clients (like the `requests` library), database clients (PostgreSQL psycopg2), Azure SDK calls (`azure-core` tracing), etc., if your code uses them ([azure-monitor-opentelemetry · PyPI](https://pypi.org/project/azure-monitor-opentelemetry/#:~:text=Instrumentation%20Supported%20library%20Name%20Supported,link%20OpenTelemetry%20Psycopg2%20Instrumentation%20psycopg2)). If you’re writing a typical data pipeline that calls external services or Azure data SDKs, those calls can be traced without manual code. It also hooks into the Python logging module so that if you log via the standard `logging` library, those logs will be captured and sent to AI (unless you disable log capture). Metrics can also be collected if you use OTel metrics APIs or if some instrumentations produce metrics.
3. **Flush and completion:** In long-running jobs, the OTel SDK will periodically batch and send telemetry (by default every 5 seconds for traces and logs in Python, as configured by environment variables like `OTEL_BSP_SCHEDULE_DELAY`). When the job finishes or the cluster shuts down, you’d want to ensure all telemetry is flushed. The SDK should flush on program exit, but you can manually force a flush if needed by shutting down the TracerProvider or ensuring the program runs to completion.

**Custom instrumentation:** If your Databricks code does something that isn’t automatically covered, you can use OpenTelemetry APIs directly in Python. For example, you can create a custom tracer and span:

```python
from opentelemetry import trace

tracer = trace.get_tracer("my_databricks_app")
with tracer.start_as_current_span("custom_step"):
    # ... your code ...
    logger.info("Processing batch X")  # this log will be inside the span's context

```

The `azure-monitor-opentelemetry` package ensures that any spans created with the OpenTelemetry API and any logs recorded via Python logging get exported to Application Insights.

**Initialize the OTel pipeline** in your code by calling `configure_azure_monitor(...).` For example:

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(connection_string="<Your AI Connection String>",
                        enable_live_metrics=False)

```

This one call sets up automatic instrumentation for supported libraries and configures exporters to send data to Azure Monitor (Application Insights). The connection string is the one you get from your Application Insights resource (it contains the instrumentation key and endpoints). If you don’t explicitly pass it, the library will look for the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable.

**Databricks-specific considerations:**

- *Cluster vs Job level:* If you have many jobs or notebooks, each can call `configure_azure_monitor`. Alternatively, you can set an **init script** on the cluster to install and configure the Azure Monitor OTel agent for the entire cluster (especially for Spark driver/JVM instrumentation). Microsoft has a sample where they attach the Java Application Insights agent to the Databricks cluster to get Spark system metrics and traces ([GitHub - Azure-Samples/databricks-observability: OpenTelemetry Demo with Azure Databricks and Azure Monitor](https://github.com/Azure-Samples/databricks-observability#:~:text=%2A%20%60git%20clone%20https%3A%2F%2Fgithub.com%2FAzure)). For Python specifically, an init script could also set environment variables globally and ensure the library is installed.
- *Data Volume:* Be mindful of how much telemetry you send from Databricks. Spark jobs can be very verbose (lots of logs for each partition/task). You might not want to send every log line to AI. Instead, focus on high-level logs (use logging levels to filter) or important custom metrics (e.g., number of records processed). The `configure_azure_monitor` function allows filtering out certain instrumentations if not needed (via `instrumentation_options`) ([azure-monitor-opentelemetry · PyPI](https://pypi.org/project/azure-monitor-opentelemetry/#:~:text=,the%20OpenTelemetry%20Resource%20associated%20with)). Also, environment vars like `OTEL_TRACES_SAMPLER_ARG` can be used to sample traces (e.g., sample = 0.5 to send only half the spans) if the volume is too high.
- *Example:* Suppose you have a Databricks job that reads from an API, transforms data, and writes to storage. By using OpenTelemetry, the HTTP calls to the API could be traced (with latency, success/failure) automatically by the `requests` instrumentation, each transformation step could log metrics (like “processed N rows”) that you send as custom metrics or logs, and any errors are logged and sent to AI. In Application Insights, you would then see those as traces and exceptions. You can query them in Log Analytics to verify job behavior or build alert rules (e.g., if a daily job fails or processes zero rows, trigger an alert based on an AI log entry).

**Other Azure Services:** The question specifically highlights Databricks, but a similar approach applies to other services:

- **Azure Functions (Python or .NET):** For .NET Functions, you can use the same `Azure.Monitor.OpenTelemetry.AspNetCore` (for in-process .NET 5/6 isolated functions, it would be similar). For Python Functions, you can call `configure_azure_monitor()` at startup of the function. As the Azure documentation notes, one should disable the built-in Functions logger to avoid double logging. The OTel SDK will capture function execution as spans and logs. There is a bit of nuance with Functions because the platform also emits its own telemetry; the recommendation is to rely solely on the OTel SDK for consistency.
- **Azure Web Apps / App Service (Java, Node, etc.):** The OpenTelemetry-based Azure Monitor offerings exist for Node.js, Java, etc., meaning you would use the respective OpenTelemetry SDKs (or Azure Monitor distro if available) in those applications similar to how we did for Python. For example, a Node.js app could use `@azure/monitor-opentelemetry` to instrument and send to AI.
- **Azure Container Apps / AKS:** If you have microservices in Kubernetes, you can run the OTel Collector or auto-instrumentation there. Microsoft’s distro is primarily about in-app SDKs right now, but in future Azure Monitor may offer an “agent” approach (there are previews of auto-instrumenting AKS with OTel without code changes ([Azure Cloud Pivots to OpenTelemetry - Observability 360](https://observability-360.com/article/ViewArticle?id=azure-opentelemetry-pivot#:~:text=360%20observability,as%20well%20as%20building))).

**Sending Logs, Metrics, and Traces:** In summary, using OpenTelemetry on these services means you can send all three kinds of telemetry to Application Insights:

- *Logs:* Any logging done in the application (e.g., using Python’s `logging` or Spark log4j) can be captured. In Python, the Azure Monitor distro captures `logging` module output by default unless disabled.
- *Metrics:* Custom metrics can be sent via OpenTelemetry’s Metrics API. Additionally, system metrics (like Spark JMX metrics) can be sent if you attach the OpenTelemetry Collector or the AI Java agent with JMX enabled. Azure Monitor can receive these as customMetrics or standard metrics.
- *Traces:* Any operation that is instrumented will produce trace spans. In Spark, for example, you might not trace each function execution by default, but you can manually create spans around major steps as shown above. External calls or database calls from the job will produce dependency spans automatically if using instrumented libraries.

All telemetry from Databricks or other services goes to your Application Insights resource, identified by the connection string/instrumentation key. On the AI side, you’ll see it intermingled with other app telemetry (if sharing) or isolated (if separate).

**Separate vs. Shared AI Instances for Databricks:** Deciding whether to use a separate Application Insights for Databricks or to share with other apps depends on use case:

- If your Databricks jobs are part of a larger application pipeline and you want a unified view of telemetry with, say, the web app that triggers the job, you might send all telemetry to one AI instance. This way, you could trace from the web request that queued a job, to the Databricks processing, to downstream results in one timeline (though in practice, linking a web app trace to a Databricks job might require passing a correlation ID manually, since Databricks jobs might not automatically pick up an Activity from an HTTP trigger unless you propagate it).
- If the Databricks environment is more of a backend batch processing that doesn’t need to be tightly correlated with interactive user requests, you might give it its own AI resource. This can be for team separation (the data engineering team monitors it separately), or to tune retention/pricing (if the Databricks logs are high-volume, you might want a shorter retention or separate billing for that telemetry).
- Sometimes, it’s useful to have separate AI for different concerns but have them use the **same Log Analytics workspace**. For instance, an e-commerce site might have AI instance “front-end” and AI instance “databricks-pipeline”, but both write to the same Log Analytics. This way, one could still correlate or query across them if needed, but they appear as separate apps in the Application Insights UI.

From a technical perspective, using a separate AI or shared doesn’t change the Databricks instrumentation code – it’s just a different connection string. It’s more about organizational clarity and data management. A rule of thumb: if different systems have different lifecycles or owners, separate instances make sense; if they are two parts of one system and frequently need combined analysis, a shared instance can simplify that.

For example, if an Azure Databricks job writes results that are immediately used by an API, and you want to trace an end-to-end transaction including the batch processing, using one AI resource helps. On the other hand, if the Databricks is doing offline analysis unrelated to the live app monitoring, keeping its telemetry separate avoids cluttering the app’s AI with batch logs.

**Integrating with Azure Databricks (Summary):** Azure Monitor’s OpenTelemetry offerings make it feasible to instrument Databricks jobs with minimal effort – a single library and function call in Python. You get the benefit of centralizing observability: your cluster’s activities can be observed in Azure Monitor alongside other components. If needed, Microsoft’s samples even cover more advanced scenarios (like capturing Spark metrics via an OpenTelemetry Collector). The decision on telemetry instance should align with how you want to query and manage the data.

## Technical Guide for Developers

This section provides some **practical configuration examples** and code snippets to help developers migrate to and set up OpenTelemetry-based Application Insights in .NET and integrate it in Azure Databricks (Python). The goal is to illustrate the changes in code and configuration.

**Migrating a .NET app to Azure.Monitor.OpenTelemetry.AspNetCore:**

*Program.cs / Startup.cs Example (ASP.NET Core 6+ minimal hosting):*

```csharp
using Azure.Monitor.OpenTelemetry.AspNetCore;  // Namespace for UseAzureMonitor extension

var builder = WebApplication.CreateBuilder(args);

// Add OpenTelemetry instrumentation and Azure Monitor exporter:
builder.Services.AddOpenTelemetry().UseAzureMonitor(o =>
{
    o.ConnectionString = "InstrumentationKey=XXXXXXXX-....;IngestionEndpoint=https://..."; 
    // Alternatively, set env var APPLICATIONINSIGHTS_CONNECTION_STRING instead of hard-coding here.
    o.SamplingRatio = 1.0f; // 100% sampling (adjust if you want to reduce volume)
});

// (Optional) Add additional OpenTelemetry configuration:
builder.Services.ConfigureOpenTelemetryTracerProvider((sp, tracerBuilder) =>
{
    tracerBuilder.AddSource("MyCompany.MyProduct.MyLibrary");  // capture custom sources
    tracerBuilder.AddGrpcClientInstrumentation();              // example: add gRPC instrumentation
});
builder.Services.ConfigureOpenTelemetryMeterProvider((sp, meterBuilder) =>
{
    meterBuilder.AddAspNetCoreInstrumentation(); // example: if you want extra metrics
});

// Add other services (MVC, etc.)
builder.Services.AddControllers();

var app = builder.Build();
app.MapControllers();
app.Run();

```

In the snippet above:

- We add the Azure Monitor OpenTelemetry **Distro** with one line (`AddOpenTelemetry().UseAzureMonitor(...)`). This replaces the old `AddApplicationInsightsTelemetry()`. It automatically includes instrumentation for incoming requests, outgoing HTTP calls, and more.
- We provide the Connection String for our Application Insights resource. This can be found in the Azure Portal for your AI resource (under **Connection String**). It includes the Instrumentation Key and endpoints. You can also use the instrumentation key directly via an older configuration, but Connection String is the recommended approach as it contains all needed info.
- The code shows setting SamplingRatio to 1.0 (meaning send all data). You could set `0.5f` to sample 50%, etc., if you want to reduce data. By default, AI Classic had adaptive sampling enabled; with OTel, you control it via this.
- The `ConfigureOpenTelemetryTracerProvider` call is optional; it demonstrates how to add a custom source or instrumentation. In this case, if you have your own `ActivitySource` in code named "MyCompany.MyProduct.MyLibrary", adding it ensures those activities are collected. We also show adding gRPC client instrumentation as an example of enabling another auto-instrumentation (assuming you installed the OTel gRPC instrumentation package).
- If you needed to add a processor or modify the resource attributes, you could do that in these configuration callbacks as well.

**Configuration via appsettings.json:** Instead of configuring in code, you can also use configuration files: In *appsettings.json*:

```json
{
  "AzureMonitor": {
    "ConnectionString": "InstrumentationKey=...;IngestionEndpoint=...;"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  }
}

```

And in code simply call `builder.Services.AddOpenTelemetry().UseAzureMonitor();` without the lambda. It will read the connection string from config by convention ([Azure Monitor Distro client library for .NET - Azure for .NET Developers | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.opentelemetry.aspnetcore-readme?view=azure-dotnet#:~:text=To%20enable%20Azure%20Monitor%20Distro%2C,from%20your%20Application%20Insights%20resource)). Logging levels can be adjusted to control what gets sent (as usual with ILogger).

After this setup, run your application. Verify in Azure Portal (Application Insights -> Live Metrics or Logs) that you see data. You can query using KQL, e.g.:

```
AppRequests | order by TimeGenerated desc | take 5

```

to see recent requests, or

```
AppTraces | where Message contains "Starting"

```

to see logs.

**Databricks (Python) Integration Example:**

Suppose you have a Databricks notebook or job in Python that you want to instrument. Here’s a simple example:

*First, install the Azure Monitor OTel package (do this in a notebook or cluster init):*

```python
# In a Databricks notebook, you can use %pip
%pip install azure-monitor-opentelemetry

```

*Next, in your application code:*

```python
from azure.monitor.opentelemetry import configure_azure_monitor
import logging

# Configure Azure Monitor OpenTelemetry
configure_azure_monitor(connection_string="InstrumentationKey=...;IngestionEndpoint=...;LiveEndpoint=...")

# (Optional) Configure Python logging level and logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MyDatabricksJob")

# Example usage
logger.info("Databricks job started")
# Simulate an external HTTP call which will be auto-tracked if using requests
import requests
response = requests.get("https://api.example.com/data")
logger.info(f"Fetched data, response code {response.status_code}")
# If we want to add a custom trace span for a computation block:
from opentelemetry import trace
tr = trace.get_tracer("MyDatabricksJob")
with tr.start_as_current_span("data_cleaning"):
    # ... data cleaning logic ...
    logger.info("Cleaned the data")

logger.warning("Databricks job finished with some warnings")

```

A few notes on this example:

- `configure_azure_monitor()` initializes the telemetry pipeline. Once called, it instruments libraries like `requests` (so the GET request will produce a dependency telemetry), and captures logs via the standard logging module.
- The connection string here should be your AI resource’s string. In Databricks, you might instead set it as an environment variable in the cluster: e.g., in the cluster Spark config: `spark.env.APPLICATIONINSIGHTS_CONNECTION_STRING` = `InstrumentationKey=...;...`. The `configure_azure_monitor` call would then pick it up automatically from env if you don’t pass it explicitly.
- We created a logger and logged messages. These will appear in Application Insights as trace log entries. The logs automatically include metadata like logger name and severity.
- We manually created a span “data\_cleaning” around a block of code to demonstrate custom tracing. If you don’t do this, it’s fine; you’ll still get a trace for the HTTP call and possibly some default trace representing the application if one was started. But creating custom spans can help break down the job’s timeline in the telemetry.
- When this job runs, you can open Log Analytics and query e.g. `AppTraces | where cloud_RoleInstance contains "databricks"` (assuming the library sets the cloud role instance to something identifying the cluster node, and possibly cloud\_RoleName to something like “UnknownHost” by default for custom environments – you might override resource attributes via `configure_azure_monitor(resource={"service.name": "MyDatabricksJob"})` if you want a custom role name).

**Databricks Spark Metrics:** If you need Spark-level metrics, one approach is to use the Java OpenTelemetry JAR. The Azure Samples repo shows attaching the Application Insights Java agent to the Databricks cluster (for the JVM). This can capture Spark telemetry (like stages, shuffle, etc.) via JMX. However, that’s an advanced scenario. Most developers can start with the Python SDK approach for logs and traces of their job’s custom code.

**Environment and Configurations:**

- You can fine-tune what is collected using environment variables as described in the PyPI docs. For example, set `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS="urllib,urllib3"` if you don’t want to auto-instrument certain libs.
- To send metrics from Python, you could use the OpenTelemetry metrics API (`from opentelemetry import metrics`) and create instruments. Those would be exported if the Azure exporter supports it. Currently, Azure Monitor exporter for Python supports traces and logs, and metrics in some capacity (it’s evolving as OTel metrics in Python stabilizes).
- **Live Metrics:** In .NET, live metrics just works if you enabled it (the distro supports it). In Python, `enable_live_metrics=True` can be passed to `configure_azure_monitor`, though Live Metrics for Python might be a preview feature.

**Validation:** After configuring, run a test job. Then in Application Insights, use **Transaction Search** or Logs to find data. If using a separate AI, you’ll only see Databricks data there. If shared, use filters (like operation name or cloud role) to isolate it.

**Telemetry Separation or Union:** If sending Databricks and app telemetry to the same AI, ensure you label the telemetry source. In .NET, as mentioned, `cloud_RoleName` is automatically like your app name. In Python, by default it might not set a service name unless you provide one. The `configure_azure_monitor` function takes a `resource` argument where you can specify `service.name` and other attributes. Setting `service.name="DatabricksJob"` will cause that value to appear as cloud\_RoleName in Application Insights. This is very useful for distinguishing telemetry from different sources when they share the same AI. If you don't set it, all custom telemetry might show up with a generic role name (which could be the hostname or "unknown\_service:python"). So it's recommended to set `service.name` or use the environment variable `OTEL_SERVICE_NAME` for clarity.

**Example KQL queries:**

- View logs from Databricks job: `AppTraces | where cloud_RoleName == "DatabricksJob" | order by TimeGenerated desc`.
- View an aggregated metric (if you logged count in logs): If you log an INFO like "Processed 1000 records", you could parse it in KQL or better, use a custom metric instrument and then query the `AppMetrics` table.
- Distributed trace example: If your Databricks job calls an API that is also instrumented and sends telemetry to AI, you can correlate by operation Id. Use `union AppRequests, AppDependencies | where operation_Id == "someID"` to see spans from both sides.

This technical setup shows that moving to OpenTelemetry doesn’t add a lot of burden – in many cases it simplifies configuration (one line to add instrumentation, one line in Python to configure). The key is understanding the new knobs (like environment variables and OTel configuration) which replace the old ApplicationInsights.config or .config settings.

## Using Log Analytics for Observability

**Log Analytics** is the workhorse for storing and querying telemetry in Azure Monitor. Once your distributed application is sending logs, traces, and metrics to Application Insights (and thus to Log Analytics), the next step is to leverage that data for observability. Different personas in an organization use Log Analytics in various ways to glean insights:

- **Site Reliability Engineers (SREs/Ops Teams):** SREs are focused on reliability, performance, and alerting. They use Log Analytics to investigate incidents and monitor the health of the system. For example, if an alert fires indicating an increase in errors, an SRE might run a query in Log Analytics to fetch all exceptions in the last hour across all services (`AppExceptions | where timestamp > ago(1h)`). They might join traces and requests to follow a correlation ID through the stack to pinpoint which service failed and why. SREs also set up **alerts** based on Log Analytics queries – for instance, an alert if more than X failures occur in 5 minutes (`AppRequests | where Success == false | summarize count() > X`). They might create **dashboards or Workbooks** with charts of latency, error rates, and throughput, all powered by KQL queries on the Log data. Log Analytics also allows SREs to do proactive analysis, like capacity planning: e.g., query how memory usage (if custom metrics were tracked) correlates with load over time.
- **Developers/Architects:** This persona uses Log Analytics to understand how the application behaves and to troubleshoot logical issues or performance bottlenecks. For instance, an architect can query **Application Map** data or directly query dependencies to see what external calls each service is making (`AppDependencies | summarize count() by target, name`). This helps verify if the architecture’s service interactions are as expected. They also review **performance data** – e.g., using Log Analytics to find the slowest requests or database calls (`AppDependencies | order by duration desc | take 10`). If a new deployment is made, developers can compare telemetry before and after via queries. They might also use logs to ensure that new code paths are executed (checking certain log messages presence). The **Application Insights “Failures” and “Performance” blades** internally run queries to show top exceptions and slowest operations; architects often drill through those into raw queries to do deeper analysis. Additionally, architects might look at **usage patterns** via custom events or funnel analysis – for example, tracking how many users go through a specific sequence (though some of that is provided by AI’s usage analytics, which can also be accessed via queries on custom events and page views). The key is that Log Analytics provides flexibility; architects are not limited to canned reports – they can slice data in whatever way needed to answer a question about the system's behavior.
- **Business Owners/Product Managers:** While business stakeholders might not use Log Analytics directly (they prefer higher-level dashboards or reports), the data in Log Analytics can be used to create those insights. For example, if the application is instrumented with custom events like “UserSignedUp” or “PurchaseCompleted”, a product manager might be interested in conversion rates or usage trends. Analysts or engineers can use KQL to extract these metrics: e.g., `customEvents | where name == "PurchaseCompleted" | summarize count() by bin(timestamp, 1d)` to see daily purchase counts. This data can be surfaced via **Azure Monitor Workbooks** or exported to Power BI. Business owners also care about SLA and uptime – Log Analytics data can be used to compute uptime percentages (looking at availability tests or request success rates) and included in reports. If a business owner wants to know the impact of an outage, a query might be run to list how many users were affected (perhaps by counting distinct user IDs in telemetry around that time). So indirectly, Log Analytics serves them through the creation of tailored queries and visualizations that answer business questions. Some personas also use the **Analytics Portal (AI)** which provides a UI for KQL and some pre-built charts for usage, but ultimately it’s the same data underneath.
- **Security and Compliance Teams:** (Not explicitly asked, but another persona) might use Log Analytics to watch for anomalous or unauthorized activities captured in logs. For instance, searching logs for certain keywords or patterns of access. Often, this overlaps with Azure Sentinel or security-specific tools, but those can ingest from Log Analytics as well.

**Consolidation of Data:** Because Log Analytics aggregates all telemetry types, users can correlate across them. For example, an SRE investigating a spike in latency can query both logs and metrics in one go: maybe retrieve the server CPU metric and the request durations and see if there’s a correlation. Or join traces with metrics to see if a particular customer ID (found in a log property) correlates with high resource usage. The unified schema (where `operation_Id` can tie together traces, dependencies, logs) is extremely powerful. Even when using multiple AI resources, if they share a workspace, you can do cross-app joins easily. This is far better than having siloed logs in different tools.

**Using Log Analytics Effectively:**

- Users often save KQL queries that are useful (there’s a feature to save queries or use the query explorer in Azure Monitor).
- They might create **Workbooks** for routine monitoring scenarios – e.g., a workbook that takes a parameter of a user session ID and then runs multiple queries (requests, dependencies, traces filtered by that session ID) to present a mini report for that session’s activity.
- **Example scenario:** An SRE gets an alert of high failure rate. They open Log Analytics and run a query to get a sample of failed requests and their operation\_Id. They pick an operation\_Id and then run another query to get all telemetry for that operation (requests, dependencies, exceptions, logs). This might show that in that operation, a specific SQL query timed out (dependency), and perhaps a custom log says "User input validation failed". From there, they involve a developer, who then uses a similar process to pinpoint the code issue. The developer might add additional logging and redeploy, and then use Log Analytics to verify the fix (by seeing that new log messages appear and the error stops happening).

**Log Analytics Query Examples by Persona:**

*Product Manager:* “How many sign-ups per day and how many completed profiles per day” (assuming those are custom events):

```kql
customEvents
| where name in ("UserSignedUp", "ProfileCompleted")
| summarize count() by name, date=format_datetime(bin(timestamp, 1d), 'yyyy-MM-dd')
| render columnchart

```

This uses Log Analytics to produce a quick chart of those business events.

*Architect:* “Show average duration of each operation name per cloud role (service) in last 1h”:

```kql
AppRequests
| where timestamp > ago(1h)
| summarize avg(duration) by cloud_RoleName, name

```

This helps spot if a particular service or API method is slower than others.

*SRE:* “What are the top 5 exceptions in the last 24h across all services?”:

```kql
AppExceptions 
| where timestamp > ago(24h) 
| summarize count() by type = innermostExceptionType, problemId 
| top 5 by count

```

This might show, for example, that NullReferenceException happened 100 times in OrdersAPI, etc.

**User Experiences:** Different personas might access this data through different interfaces:

- SREs/Devs: Azure Portal’s Logs blade (KQL editor) or using tools like Azure Data Explorer Web UI for more complex queries, or even VS Code plugins for Kusto.
- Business: likely through Workbooks or integrated dashboards. Azure Application Insights has a feature called "Workbook" which can present data in a friendly way. You can create a workbook that surfaces key metrics (from Log Analytics queries) with visualizations and text, tailored for a less technical audience. For example, a workbook for “Release Health” that shows number of errors, user sessions, and revenue (if tracked) before vs after a deployment.

**Closing notes on Observability:** Log Analytics is the backbone that **consolidates logs, traces, and metrics** ([Application Insights OpenTelemetry overview - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview#:~:text=,that%20visualize%20application%20monitoring%20data)). By having all this telemetry in one queryable store, Azure Monitor supports a comprehensive observability approach:

- You *monitor* by setting alerts on metrics and logs.
- You *visualize* through dashboards and workbooks.
- You *trace and debug* by drilling into correlated telemetry.
- You *learn and optimize* by analyzing usage patterns and performance trends over time.

Each persona contributes to the feedback loop: SREs ensure reliability (which feeds into product quality), developers fix and optimize using telemetry evidence, and business owners steer the product with insights drawn from usage data. Log Analytics, combined with Application Insights and OpenTelemetry instrumentation, provides the data and tooling to make this possible. It shifts observability from being just an ops concern to a cross-disciplinary practice where everyone can get the information they need from the running system, in near real-time, with the flexibility of powerful query and analysis capabilities. ([Application Insights OpenTelemetry overview - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview#:~:text=Application%20Insights%20Experiences)) ([Application Insights OpenTelemetry overview - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview#:~:text=,that%20visualize%20application%20monitoring%20data))
