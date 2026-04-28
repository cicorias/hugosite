---
title: "Using a WCF Message Inspector to extend AppFabric Monitoring"
date: 2010-06-10T10:42:06+0000
lastmod: 2010-06-10T10:42:06+0000
slug: "using-a-wcf-message-inspector-to-extend-appfabric-monitoring"
aliases:
  - /using-a-wcf-message-inspector-to-extend-appfabric-monitoring/
---

I read through Ron Jacobs post on Monitoring WCF Data Services with AppFabric

[http://blogs.msdn.com/b/endpoint/archive/2010/06/09/tracking-wcf-data-services-with-windows-server-appfabric.aspx](http://blogs.msdn.com/b/endpoint/archive/2010/06/09/tracking-wcf-data-services-with-windows-server-appfabric.aspx "http://blogs.msdn.com/b/endpoint/archive/2010/06/09/tracking-wcf-data-services-with-windows-server-appfabric.aspx")

What is immediately striking are 2 things – it’s so easy to get monitoring data into a viewer (AppFabric Dashboard) w/ very little work.  And the 2nd thing is, why can’t this be a WCF message inspector on the dispatch side.

So, I took the base class **WCFUserEventProvider** that’s located in the WCF/WF samples [[1]](http://www.microsoft.com/downloads/details.aspx?FamilyID=35ec8682-d5fd-4bc3-a51a-d8ad115a8792&displaylang=en) in the following path, \WF\_WCF\_Samples\WCF\Basic\Management\AnalyticTraceExtensibility\CS\WCFAnalyticTracingExtensibility\  and then created a few classes that project the injection as a IEndPointBehavior

There are just 3 classes to drive injection of the inspector at runtime via config:

1. IDispatchMessageInspector implementation
2. BehaviorExtensionElementimplementation
3. IEndpointBehavior implementation

The full source code is below with a link to the solution file here: [[Solution File](http://cicoria.com/downloads/AppFabricMonitoringWcfInspector.zip)]

```
    public object AfterReceiveRequest(
        ref Message request,
        IClientChannel channel,
        InstanceContext instanceContext)
    {

        OperationContext ctx = OperationContext.Current;
        var opName = ctx.IncomingMessageHeaders.Action;

        evntProvider.WriteInformationEvent(&quot;start&quot;, string.Format(&quot;operation: {0} at address {1}&quot;, opName, ctx.EndpointDispatcher.EndpointAddress));
        return null;
    }

    public void BeforeSendReply(ref System.ServiceModel.Channels.Message reply, object correlationState)
    {
        OperationContext ctx = OperationContext.Current;
        var opName = ctx.IncomingMessageHeaders.Action;

        evntProvider.WriteInformationEvent(&quot;end&quot;, string.Format(&quot;operation: {0} at address {1}&quot;, opName, ctx.EndpointDispatcher.EndpointAddress));
        
    }
}

public class AppFabricE2EBehaviorElement : BehaviorExtensionElement
{

    #region BehaviorExtensionElement
    /// &lt;summary&gt;
    /// Gets the type of behavior.
    /// &lt;/summary&gt;
    /// &lt;value&gt;&lt;/value&gt;
    /// &lt;returns&gt;The type that implements the end point behavior&lt;see cref=&quot;T:System.Type&quot;/&gt;.&lt;/returns&gt;
    public override Type BehaviorType
    {
        get { return typeof(AppFabricE2EEndpointBehavior); }
    }

    /// &lt;summary&gt;
    /// Creates a behavior extension based on the current configuration settings.
    /// &lt;/summary&gt;
    /// &lt;returns&gt;The behavior extension.&lt;/returns&gt;
    protected override object CreateBehavior()
    {
        return new AppFabricE2EEndpointBehavior();
    }

    #endregion BehaviorExtensionElement

}

public class AppFabricE2EEndpointBehavior : IEndpointBehavior //, IServiceBehavior
{

    #region IEndpointBehavior
    public void AddBindingParameters(ServiceEndpoint endpoint, BindingParameterCollection bindingParameters) {}

    public void ApplyClientBehavior(ServiceEndpoint endpoint, ClientRuntime clientRuntime)
    {
        throw new NotImplementedException();
    }

    public void ApplyDispatchBehavior(ServiceEndpoint endpoint, EndpointDispatcher endpointDispatcher)
    {
        endpointDispatcher.DispatchRuntime.MessageInspectors.Add(new AppFabricE2EInspector());

    }

    public void Validate(ServiceEndpoint endpoint)
    {
        ;
    }
    #endregion IEndpointBehavior

}

```

[1] [http://www.microsoft.com/downloads/details.aspx?FamilyID=35ec8682-d5fd-4bc3-a51a-d8ad115a8792&displaylang=en](http://www.microsoft.com/downloads/details.aspx?FamilyID=35ec8682-d5fd-4bc3-a51a-d8ad115a8792&displaylang=en "http://www.microsoft.com/downloads/details.aspx?FamilyID=35ec8682-d5fd-4bc3-a51a-d8ad115a8792&displaylang=en")
