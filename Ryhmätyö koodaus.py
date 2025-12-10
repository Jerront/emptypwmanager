import koulu as k

# Ensure clean state
k.websites.clear()
k.usernames.clear()
k.encrypted_passwords.clear()

# Add and retrieve
assert k.add_password('site.xyz','alice','S3cure!pw')
u, p = k.get_password('site.xyz')
assert u == 'alice'
assert p == 'S3cure!pw'

# Save and load
k.save_passwords()
data = k.load_passwords()
assert any(item.get('website') == 'site.xyz' for item in data)

print('All checks passed')
