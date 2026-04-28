---
title: "Making Web Client requests behave from .NET or in reality misbehave – ignoring Certificate Issues from HttpWebRequest"
date: 2010-09-05T04:39:14+0000
lastmod: 2010-09-05T04:39:14+0000
slug: "making-web-client-requests-behave-from-net-or-in-reality-misbehave-ignoring-certificate-issues-from-httpwebrequest"
aliases:
  - /making-web-client-requests-behave-from-net-or-in-reality-misbehave-ignoring-certificate-issues-from-httpwebrequest/
---

Many times, especially during development, you could have certificates that are out of date, aren’t singed by any real authority (makecert, etc.), or even don’t match the host name that the request is issued against, but you want to test, etc.

One example is if you want to run Fiddler to get a good over-the-wire trace of the HTTP traffic, when the endpoint is accessed over HTTPS.  With Fiddler, you can capture HTTPS traffic, only thing is, it sticks it’s own certificate in the chain which doesn't match the DNS name of the host.  So, your HttpWebRequest call will fail regardless.

So, to have HttpWebRequest ignore all errors (this is testing only mode – don’t do this in production – or do it carefully) establish the certificate validation callback using the following – which basically, regardless of the SSL Policy error, just returns “true” – basically, nothing is ever wrong.

```
public class AcceptAllCertificates
{
    public AcceptAllCertificates()
    {
        System.Net.ServicePointManager.ServerCertificateValidationCallback +=
            ((sender, certificate, certicateChain, sslPolicyErrors) => true);
    }
}
```

The key thing is, this becomes over-arching – that means, SerivcePointManager now implements this policy across all subsequent calls.  You need to call this at application startup, or somewhere before issuing requests. You can extend this and implement your own rules, but this is something I just used to take a good Fiddler trace against an external HTTPS endpoint that I didn’t control without having exceptions tossed.

There are a whole bunch of other things that you can take advantage of in ServicePointManager – things such as the HttpConnection limit, which is based upon a W3 spec, but for internal back-end service calls over REST and the like, you may want to affect.

```
namespace System.Net
{
    // Summary:
    //     Manages the collection of System.Net.ServicePoint objects.
    public class ServicePointManager
    {
        // Summary:
        //     The default number of non-persistent connections (4) allowed on a System.Net.ServicePoint
        //     object connected to an HTTP/1.0 or later server. This field is constant but
        //     is no longer used in the .NET Framework 2.0.
        public const int DefaultNonPersistentConnectionLimit = 4;
        //
        // Summary:
        //     The default number of persistent connections (2) allowed on a System.Net.ServicePoint
        //     object connected to an HTTP/1.1 or later server. This field is constant and
        //     is used to initialize the System.Net.ServicePointManager.DefaultConnectionLimit
        //     property if the value of the System.Net.ServicePointManager.DefaultConnectionLimit
        //     property has not been set either directly or through configuration.
        public const int DefaultPersistentConnectionLimit = 2;

        // Summary:
        //     Gets or sets policy for server certificates.
        //
        // Returns:
        //     An object that implements the System.Net.ICertificatePolicy interface.
        [Obsolete("CertificatePolicy is obsoleted for this type, please use ServerCertificateValidationCallback instead. http://go.microsoft.com/fwlink/?linkid=14202")]
        public static ICertificatePolicy CertificatePolicy { get; set; }
        //
        // Summary:
        //     Gets or sets a System.Boolean value that indicates whether the certificate
        //     is checked against the certificate authority revocation list.
        //
        // Returns:
        //     true if the certificate revocation list is checked; otherwise, false.
        public static bool CheckCertificateRevocationList { get; set; }
        //
        // Summary:
        //     Gets or sets the maximum number of concurrent connections allowed by a System.Net.ServicePoint
        //     object.
        //
        // Returns:
        //     The maximum number of concurrent connections allowed by a System.Net.ServicePoint
        //     object. The default value is 2.
        //
        // Exceptions:
        //   System.ArgumentOutOfRangeException:
        //     System.Net.ServicePointManager.DefaultConnectionLimit is less than or equal
        //     to 0.
        public static int DefaultConnectionLimit { get; set; }
        //
        // Summary:
        //     Gets or sets a value that indicates how long a Domain Name Service (DNS)
        //     resolution is considered valid.
        //
        // Returns:
        //     The time-out value, in milliseconds. A value of -1 indicates an infinite
        //     time-out period. The default value is 120,000 milliseconds (two minutes).
        public static int DnsRefreshTimeout { get; set; }
        //
        // Summary:
        //     Gets or sets a value that indicates whether a Domain Name Service (DNS) resolution
        //     rotates among the applicable Internet Protocol (IP) addresses.
        //
        // Returns:
        //     false if a DNS resolution always returns the first IP address for a particular
        //     host; otherwise true. The default is false.
        public static bool EnableDnsRoundRobin { get; set; }
        //
        // Summary:
        //     Gets the System.Net.Security.EncryptionPolicy for this System.Net.ServicePointManager
        //     instance.
        //
        // Returns:
        //     The encryption policy to use for this System.Net.ServicePointManager instance.
        public static EncryptionPolicy EncryptionPolicy { get; }
        //
        // Summary:
        //     Gets or sets a System.Boolean value that determines whether 100-Continue
        //     behavior is used.
        //
        // Returns:
        //     true to enable 100-Continue behavior. The default value is true.
        public static bool Expect100Continue { get; set; }
        //
        // Summary:
        //     Gets or sets the maximum idle time of a System.Net.ServicePoint object.
        //
        // Returns:
        //     The maximum idle time, in milliseconds, of a System.Net.ServicePoint object.
        //     The default value is 100,000 milliseconds (100 seconds).
        //
        // Exceptions:
        //   System.ArgumentOutOfRangeException:
        //     System.Net.ServicePointManager.MaxServicePointIdleTime is less than System.Threading.Timeout.Infinite
        //     or greater than System.Int32.MaxValue.
        public static int MaxServicePointIdleTime { get; set; }
        //
        // Summary:
        //     Gets or sets the maximum number of System.Net.ServicePoint objects to maintain
        //     at any time.
        //
        // Returns:
        //     The maximum number of System.Net.ServicePoint objects to maintain. The default
        //     value is 0, which means there is no limit to the number of System.Net.ServicePoint
        //     objects.
        //
        // Exceptions:
        //   System.ArgumentOutOfRangeException:
        //     System.Net.ServicePointManager.MaxServicePoints is less than 0 or greater
        //     than System.Int32.MaxValue.
        public static int MaxServicePoints { get; set; }
        //
        // Summary:
        //     Gets or sets the security protocol used by the System.Net.ServicePoint objects
        //     managed by the System.Net.ServicePointManager object.
        //
        // Returns:
        //     One of the values defined in the System.Net.SecurityProtocolType enumeration.
        //
        // Exceptions:
        //   System.NotSupportedException:
        //     The value specified to set the property is not a valid System.Net.SecurityProtocolType
        //     enumeration value.
        public static SecurityProtocolType SecurityProtocol { get; set; }
        //
        // Summary:
        //     Gets or sets the callback to validate a server certificate.
        //
        // Returns:
        //     A System.Net.Security.RemoteCertificateValidationCallback The default value
        //     is null.
        public static RemoteCertificateValidationCallback ServerCertificateValidationCallback { get; set; }
        //
        // Summary:
        //     Determines whether the Nagle algorithm is used by the service points managed
        //     by this System.Net.ServicePointManager object.
        //
        // Returns:
        //     true to use the Nagle algorithm; otherwise, false. The default value is true.
        public static bool UseNagleAlgorithm { get; set; }

        // Summary:
        //     Finds an existing System.Net.ServicePoint object or creates a new System.Net.ServicePoint
        //     object to manage communications with the specified System.Uri object.
        //
        // Parameters:
        //   address:
        //     The System.Uri object of the Internet resource to contact.
        //
        // Returns:
        //     The System.Net.ServicePoint object that manages communications for the request.
        //
        // Exceptions:
        //   System.ArgumentNullException:
        //     address is null.
        //
        //   System.InvalidOperationException:
        //     The maximum number of System.Net.ServicePoint objects defined in System.Net.ServicePointManager.MaxServicePoints
        //     has been reached.
        [TargetedPatchingOptOut("Performance critical to inline this type of method across NGen image boundaries")]
        public static ServicePoint FindServicePoint(Uri address);
        //
        // Summary:
        //     Finds an existing System.Net.ServicePoint object or creates a new System.Net.ServicePoint
        //     object to manage communications with the specified Uniform Resource Identifier
        //     (URI).
        //
        // Parameters:
        //   uriString:
        //     The URI of the Internet resource to be contacted.
        //
        //   proxy:
        //     The proxy data for this request.
        //
        // Returns:
        //     The System.Net.ServicePoint object that manages communications for the request.
        //
        // Exceptions:
        //   System.UriFormatException:
        //     The URI specified in uriString is invalid.
        //
        //   System.InvalidOperationException:
        //     The maximum number of System.Net.ServicePoint objects defined in System.Net.ServicePointManager.MaxServicePoints
        //     has been reached.
        public static ServicePoint FindServicePoint(string uriString, IWebProxy proxy);
        //
        // Summary:
        //     Finds an existing System.Net.ServicePoint object or creates a new System.Net.ServicePoint
        //     object to manage communications with the specified System.Uri object.
        //
        // Parameters:
        //   address:
        //     A System.Uri object that contains the address of the Internet resource to
        //     contact.
        //
        //   proxy:
        //     The proxy data for this request.
        //
        // Returns:
        //     The System.Net.ServicePoint object that manages communications for the request.
        //
        // Exceptions:
        //   System.ArgumentNullException:
        //     address is null.
        //
        //   System.InvalidOperationException:
        //     The maximum number of System.Net.ServicePoint objects defined in System.Net.ServicePointManager.MaxServicePoints
        //     has been reached.
        public static ServicePoint FindServicePoint(Uri address, IWebProxy proxy);
        //
        // Summary:
        //     Enables or disables the keep-alive option on a TCP connection.
        //
        // Parameters:
        //   enabled:
        //     If set to true, then the TCP keep-alive option on a TCP connection will be
        //     enabled using the specified keepAliveTime and keepAliveInterval values. If
        //     set to false, then the TCP keep-alive option is disabled and the remaining
        //     parameters are ignored.The default value is false.
        //
        //   keepAliveTime:
        //     Specifies the timeout, in milliseconds, with no activity until the first
        //     keep-alive packet is sent.The value must be greater than 0. If a value of
        //     less than or equal to zero is passed an System.ArgumentOutOfRangeException
        //     is thrown.
        //
        //   keepAliveInterval:
        //     Specifies the interval, in milliseconds, between when successive keep-alive
        //     packets are sent if no acknowledgement is received.The value must be greater
        //     than 0. If a value of less than or equal to zero is passed an System.ArgumentOutOfRangeException
        //     is thrown.
        //
        // Exceptions:
        //   System.ArgumentOutOfRangeException:
        //     The value specified for keepAliveTime or keepAliveInterval parameter is less
        //     than or equal to 0.
        public static void SetTcpKeepAlive(bool enabled, int keepAliveTime, int keepAliveInterval);
    }
}
```
