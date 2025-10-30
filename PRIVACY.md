# Privacy Policy for SheetAlchemy

**Last Updated: October 30, 2025**

This Privacy Policy describes how SheetAlchemy (Google Sheets Object Data Model) handles data and privacy considerations when using this library.

## 🔒 Overview

SheetAlchemy is an open-source Python library that provides an interface to Google Sheets. This privacy policy explains how data flows through the library and what developers should consider when using SheetAlchemy in their applications.

## 📊 Data Handling

### What SheetAlchemy Does

SheetAlchemy acts as a **client-side library** that:

- Connects to Google Sheets API on behalf of your application
- Reads data from Google Sheets that you have authorized access to
- Processes and transforms sheet data locally within your application
- Does **NOT** store, collect, or transmit your data to any external servers (except Google Sheets API)

### Data Flow

```
Your Application → SheetAlchemy Library → Google Sheets API → Google Sheets
```

1. **Authentication**: Your application provides Google API credentials
2. **Data Retrieval**: SheetAlchemy uses these credentials to fetch data from specified Google Sheets
3. **Local Processing**: All data transformation and filtering happens locally in your application
4. **No External Storage**: SheetAlchemy does not persist or transmit data to any third-party services

## 🔐 Authentication and Credentials

### Service Account Keys

SheetAlchemy requires Google Service Account credentials to access Google Sheets:

- **Your Responsibility**: Securely store and manage your service account key files
- **Best Practices**: 
  - Never commit key files to version control
  - Use environment variables for key file paths
  - Restrict service account permissions to minimum required access
  - Regularly rotate service account keys

### Google Sheets Access

SheetAlchemy can only access Google Sheets that:
- Are explicitly shared with your service account email
- Have appropriate permissions (read, write as needed)
- Are accessible through the Google Sheets API

## 🛡️ Security Considerations

### For Developers Using SheetAlchemy

1. **Credential Security**
   ```python
   # ✅ Good: Use environment variables
   import os
   key_path = os.environ.get('GODM_AUTH_KEY_PATH')
   
   # ❌ Bad: Hardcoded paths in code
   key_path = '/path/to/secret/key.json'
   ```

2. **Access Control**
   - Only share sheets with service accounts that need access
   - Use least-privilege principle for service account permissions
   - Regularly audit sheet sharing permissions

3. **Data Validation**
   ```python
   # Always validate and sanitize data from sheets
   user = Users.manager.get(name="John")
   errors = user.get_errors()
   if errors:
       # Handle validation errors appropriately
       logging.warning(f"Data validation errors: {errors}")
   ```

### For End Users

If you're using an application built with SheetAlchemy:

- The application developer is responsible for data privacy and security
- SheetAlchemy itself does not collect or store your personal data
- Review the privacy policy of the specific application you're using

## 📋 Data Processing

### Local Processing Only

SheetAlchemy performs all operations locally:

- **Field Validation**: Type checking and format validation
- **Data Transformation**: Converting strings to dates, numbers, etc.
- **Query Processing**: Filtering and searching through data
- **Caching**: Temporary storage in application memory only

### No Data Collection

SheetAlchemy does **NOT**:
- Collect usage analytics or telemetry
- Store user data on external servers  
- Share data with third parties
- Track user behavior or application usage

## 🌍 Third-Party Services

### Google Sheets API

SheetAlchemy integrates with Google Sheets API:

- **Purpose**: Reading and writing sheet data
- **Data Shared**: Only the sheet data you explicitly access
- **Google's Policies**: Subject to [Google's Privacy Policy](https://policies.google.com/privacy)
- **Your Control**: You control which sheets are accessible and what data is shared

### Dependencies

SheetAlchemy relies on:
- **gspread**: Python library for Google Sheets API (follows same privacy principles)
- **Python Standard Library**: No additional privacy implications

## 📱 Application Developer Responsibilities

If you're building applications with SheetAlchemy:

### Privacy Compliance

1. **Create Your Own Privacy Policy**: SheetAlchemy's policy does not cover your application
2. **Data Handling**: Implement appropriate data protection measures
3. **User Consent**: Obtain necessary permissions for accessing user data
4. **Compliance**: Follow applicable laws (GDPR, CCPA, etc.)

### Best Practices

```python
# Example: Implementing data minimization
class UserModel(GModel):
    # Only include fields you actually need
    name = StringField(name="Name")
    # Don't include sensitive fields unless necessary
    
    class Meta:
        sheet_name = "Users"
        tab_name = "PublicData"  # Use appropriate sheet sections
```

### Recommended Policies

1. **Data Retention**: Delete cached data when no longer needed
2. **Access Logging**: Log data access for security auditing
3. **Error Handling**: Don't expose sensitive data in error messages
4. **User Rights**: Provide ways for users to access, update, or delete their data

## 🔍 Data Minimization

### Built-in Features

SheetAlchemy supports data minimization through:

```python
# Load only when needed
class LazyModel(GModel):
    class Meta:
        load_policy = LoadPolicy.LAZY

# Filter data to reduce memory usage  
specific_users = Users.manager.filter(department="Engineering")

# Access only required fields
user_names = [user.name for user in Users.manager.filter(active=True)]
```

## 📞 Contact Information

### For SheetAlchemy Library Issues

- **GitHub Issues**: [https://github.com/0xdps/g-odm/issues](https://github.com/0xdps/g-odm/issues)
- **Security Issues**: Contact maintainer directly via GitHub
- **General Questions**: Use GitHub Discussions

### For Application-Specific Privacy Questions

Contact the developer of the specific application you're using, not the SheetAlchemy maintainers.

## 🔄 Updates to This Policy

This privacy policy may be updated to reflect:
- Changes in SheetAlchemy functionality
- Legal requirements
- Best practice improvements

**How You'll Be Notified**:
- Updates posted to GitHub repository
- Version changes noted in release notes
- Major changes announced in project communications

## ⚖️ Legal Considerations

### Disclaimer

SheetAlchemy is provided "as is" without warranties. Users are responsible for:
- Complying with applicable privacy laws
- Implementing appropriate security measures
- Protecting user data in their applications

### Limitation of Liability

The SheetAlchemy maintainers are not responsible for:
- How developers use the library
- Privacy practices of applications built with SheetAlchemy
- Data breaches in applications using SheetAlchemy
- Compliance with privacy regulations by third parties

## 🌐 International Considerations

### Data Transfers

When using SheetAlchemy:
- Data flows between your application and Google Sheets
- Google Sheets data may be stored in various Google data centers globally
- Refer to [Google's data transfer policies](https://cloud.google.com/terms/data-transfer-practices) for details

### Regional Compliance

Developers should consider:
- **GDPR** (EU): Right to access, rectification, erasure, portability
- **CCPA** (California): Consumer privacy rights and disclosures  
- **Other Regulations**: Local data protection laws in your jurisdiction

---

## 📋 Summary

- **SheetAlchemy is a client-side library** that doesn't collect or store user data
- **All data processing happens locally** in your application
- **Developers are responsible** for privacy practices in their applications  
- **Google Sheets API** is the only external service SheetAlchemy communicates with
- **Security is shared responsibility** between SheetAlchemy, developers, and users

For questions about this privacy policy, please open an issue on GitHub.

---

**This privacy policy applies specifically to the SheetAlchemy library. Applications built using SheetAlchemy may have their own privacy policies and practices.**