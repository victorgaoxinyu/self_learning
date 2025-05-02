## IAM: User & Groups

- IAM: Identity and Access Management, Global service
- Root account:created by default, shouldn't be used or shared
- Users: people within org, can be grouped
- Groups: only contain users, **not** other groups
- Users dont have to belong to a group, and user can be long to multiple groups

## IAM: Permissions
- Users or Groups can be assigned JSON doc called policies
- Polcies define permission of the users
- Inline policy that directly attached to user
- Group policy attach to user via group
- In AWS **least privilege principle** is applied. dont give user more permissons than a user needs

## IAM Policies
- Structure
  - Version: policy lanaguage version
  - Id: identifier for policy (optional)
  - Statement: one ore more individual statements, `List[Dict]` (required)
- Statement structure:
  - Sid: identifier for the statement (optional)
  - Effect: Allow, Deny
  - Principal: account/user/role to which this policy applied to
  - Action: list of actions this policy allows or denies
  - Resource: list of resources to which the actions applied to
  - Condition: conditions for when this policy is in effect (optional)

## IAM Password Policy
- set up minimum password length
- require specific types:
  - including upper/lower case
  - numbers
  - non-alphanumeric characters
- Allow all IAM users to change their own passwords
- Password expiration
- Prevent password re-use

## IMA MFA Multi Factor Authentication
- MFA = password you known + security device you own
- Benefit:
  - if a password is stolen or hacked, the account is not compromised
- Options:
  - Virtual MFA device, support multiple tokens on a single device
    - google auth
    - Authy
  - Universal 2nd Factor (U2F) Security Key, support multiple root and IAM users using single security key
    - Yubikey (3rd party)
  - Hardware Key Fob MFA Device
    - Gemalto (3rd party)
  - (US only) AWS GovCloud
    - SurePassID (3rd party)

## Access AWS
- AWS Management Console
  - password + MFA
- AWS CLI
  - access keys
- AWS SDK
  - access keys
