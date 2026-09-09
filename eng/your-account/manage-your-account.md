---
description: Manage your %%APPNAME%% account details and account-based research settings.
---

# Manage your account

Your account area helps you keep your profile details up to date and manage your personalised research features.

## Open your account area

1. Log in to %%APPNAME%%.
2. Click on your name in the top-right menu and click **My Account**.

## What you can manage

(% if AUTHOTP %)

- Account details such as your name and email address.
- Your password (you can set one if you prefer to log in with a password instead of an email code).
(% else %)
- Account details such as your name, email address, and password.
(% endif %)
(% if PAID_SUBSCRIPTIONS %)
- Your individual subscription, billing details and discounts.
(% endif %)
(% if ORGANISATION_SUBSCRIPTIONS %)
- Your organisation invitations, role and privacy information.
(% endif %)
- Account closure if you decide to [delete your account](delete-your-account.md).

(% if ORGANISATION_SUBSCRIPTIONS %)
## Manage an organisation connection

The **Organisation** section shows any organisation invitation sent to the email address on your account. Click **Review invitation** to see the proposed role, plan and privacy setting before you accept it.

After you join, this section shows:

- your organisation and role;
- whether the organisation provides your plan;
- the organisation's privacy setting and what administrators can see; and
- an option to leave the organisation, if your role allows it.

If you are the owner or an administrator, click **Manage [organisation name]** to manage members, seats and billing.

Learn more about [My LawLibrary for Organisations and Chambers](../subscription-management/organisations-and-chambers.md).
(% endif %)
