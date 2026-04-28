---
title: "Updating email address for SharePoint online users if they’re a Live / Microsoft Account…"
date: 2013-11-20T09:57:36+0000
lastmod: 2013-11-20T09:57:36+0000
slug: "updating-email-address-for-sharepoint-online-users-if-theyre-a-live-microsoft-account"
aliases:
  - /updating-email-address-for-sharepoint-online-users-if-theyre-a-live-microsoft-account/
---

If you have a SharePoint online ()365) site, and you invite users that logon with a “Microsoft Account”, those users won’t be able to receive email.  Things such as alerts won’t work.

However, you can run the code below and it will parse out all users that are “invitees” and part of the Microsoft account structure (Live.com) and just update their email, based upon what their Microsoft Account email address is.

Note: use this at your own risk.  This makes use of logon via Forms/Claims that is part of the solution here:

Remote Authentication in SharePoint Online Using the Client Object Model

<http://code.msdn.microsoft.com/Remote-Authentication-in-b7b6f43c>

Full solution is here: [Solution](https://www.cicoria.com/downloads/UpdateLiveUsersInSPOEmailAddress.zip)

```
                ctx.ExecuteQuery(); // Execute
                ListSiteUsers(ctx);
            }
        }
        Console.WriteLine("Press enter to exit...");
        Console.ReadLine();
    }

    static void ListSiteUsers(ClientContext ctx)
    {
        var users = ctx.Web.SiteUsers.AsQueryable();

        foreach (var user in users)
        {
            ctx.Load(user, u =&gt; u.UserId);
            ctx.ExecuteQuery();
            if (user.UserId == null)
            {
                string[] parts = user.LoginName.Split('|');
                if (parts.Length == 3 &amp;&amp; parts[1].Equals("membership", StringComparison.InvariantCultureIgnoreCase))
                    UpdateUser(ctx, user, parts[2]);
            }

        }
    }

    static void UpdateUser(ClientContext ctx, User user, string liveId)
    {
        string[] parts = liveId.Split('#');

        var email = parts[1];

        Console.WriteLine("user: {0}  email: {1}", user.LoginName, email);
        var userToUpdate = ctx.Web.SiteUsers.GetByLoginName(user.LoginName);
        user.Context.ExecuteQuery();
        if (null != userToUpdate)
        {
            userToUpdate.Email = email;
            userToUpdate.Update();
            ctx.ExecuteQuery();
        }
        else
            Console.WriteLine("User was null: {0}", user.LoginName);
    }

}

```
