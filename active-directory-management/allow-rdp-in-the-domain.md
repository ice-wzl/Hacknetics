# Allow RDP in the domain

1.  Start → Run → `secpol.msc`

    Security Settings\Local Policies\User Rights Assignment

    Right pane → double-click on **Allow log on through Remote Desktop Services** → Add Users or Group → enter `Remote Desktop Users`
2.  Start → Run → `services.msc`

    Look for **Remote Desktop Services** and make sure the Log on account is Network Service, not Local System.
3. Check your event logs.
