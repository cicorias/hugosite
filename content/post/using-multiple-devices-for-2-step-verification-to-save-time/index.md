---
title: "Using Multiple Devices for 2-step verification to save time !"
date: 2015-09-10T01:11:00+0000
lastmod: 2015-09-10T01:11:00+0000
slug: "using-multiple-devices-for-2-step-verification-to-save-time"
aliases:
  - /using-multiple-devices-for-2-step-verification-to-save-time/
---

[2-step verification](https://en.wikipedia.org/wiki/Multi-factor_authentication) is becoming more prevalent. This is the process where when you logon to a web site, or application, you might provide something you know (username & password) and then using a special "Authenticator" application that might be on your phone, keychain, or even your computer, you enter a challenge code.

This approach has been around for decades. If you recall the old RSA SecurID cards, now keyfobs, now soft-keyfobs that exist they use a similar principle.

These token generators basically, using the current date + time, plus some "seed" value, they both apply the same algorithm [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) that generates a numeric code (usually 6 digits) that when presented on the OTP device, you enter on the site.

In some instances, like with Azure Authentication, you can have a notification sent to your device that the App there will just ask you to Verify. Some configurations of Azure Authentication (like with MSIT) we have to supply a PIN in addition.

### Links to apps

The following are links for several of the following used. They all implement the same base algorithm and for some the source code is public.

- Google Authenticator - <https://support.google.com/accounts/answer/1066447?hl=en>
- Google Authenticator for Win 8/10 <https://www.microsoft.com/en-us/store/apps/google-authenticator/9wzdncrdnkrf>
- Azure Authenticator - <https://azure.microsoft.com/en-us/documentation/articles/multi-factor-authentication-azure-authenticator/>
- OTP Manager (Max OSX) - <https://itunes.apple.com/us/app/otp-manager/id928941247?mt=12>

## How this applies

So, the example I'm providing here works well with Github and allows you to have several devices that will all provide the same Token at time of challenge. I've been running this for a while and so far, they are all generarting the same TOken at the same time for the same (or very close) grace period.

[![](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/1258.2015-09-10_08-14-03.png)](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/1258.2015-09-10_08-14-03.png)

## Making life simple

Now, If i'm on my Mac, or only have either my iPhone, or Nexus, and if say Azure Authenticator app isn't working say for a recent update (this happens), you have a backup.

You can see here how they are all the same code...

## Setup

The setup requires a little coordination. You need to have each OTP program ready. So, on my iPhone and Nexus I have Google Authenticator, Azure Authenticator, on Mac I have OTP Manager, and Windows 10 - well, nothing yet.

1. First line up all up
2. Get to the point in Github where it's showing you the QR code
3. Then, for the phone apps, you can just start the add process and just point at the QR code
4. For the Mac or PC base app, you need to get the long "code" that you can either cut & paste into the OTP app or just type it in.
