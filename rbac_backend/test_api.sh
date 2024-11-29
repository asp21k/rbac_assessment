#!/bin/bash

# Base URL
BASE_URL="http://localhost:8000/api"
ACCESS_TOKEN=""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print response
print_response() {
    if [ $1 -eq 200 ] || [ $1 -eq 201 ]; then
        echo -e "${GREEN}Success${NC} (Status: $1)"
    else
        echo -e "${RED}Failed${NC} (Status: $1)"
    fi
    echo "$2" | python -m json.tool
}

# Test 1: Login as Super Admin
echo "Testing Super Admin Login..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{"email":"asp21k@outlook.com","password":"asp21k.."}')
ACCESS_TOKEN=$(echo $RESPONSE | python -m json.tool | grep access | cut -d '"' -f 4)
print_response $? "$RESPONSE"

# Test 2: Add permission "manage_roles"
echo -e "\nAdding permission 'manage_roles'..."
RESPONSE=$(curl -s -X POST "$BASE_URL/permissions/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"manage_roles","description":"Permission to manage roles"}')
MANAGE_ROLES_ID=$(echo $RESPONSE | python -m json.tool | grep '"id"' | head -n 1 | cut -d ':' -f 2 | tr -d ' ,')
print_response $? "$RESPONSE"

# Test 3: Add permission "manage_users"
echo -e "\nAdding permission 'manage_users'..."
RESPONSE=$(curl -s -X POST "$BASE_URL/permissions/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"manage_users","description":"Permission to manage users"}')
MANAGE_USERS_ID=$(echo $RESPONSE | python -m json.tool | grep '"id"' | head -n 1 | cut -d ':' -f 2 | tr -d ' ,')
print_response $? "$RESPONSE"

# Test 4: Create role "admin" with both permissions
echo -e "\nCreating role 'admin' with permissions..."
RESPONSE=$(curl -s -X POST "$BASE_URL/roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"admin\",\"description\":\"Admin role\",\"permission_ids\":[${MANAGE_ROLES_ID},${MANAGE_USERS_ID}]}")
ADMIN_ROLE_ID=$(echo $RESPONSE | python -m json.tool | grep '"id"' | head -n 1 | cut -d ':' -f 2 | tr -d ' ,')
print_response $? "$RESPONSE"

# Test 5: Assign "admin" role to Super Admin
echo -e "\nAssigning 'admin' role to Super Admin..."
RESPONSE=$(curl -s -X POST "$BASE_URL/user-roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"user\":1,\"role\":${ADMIN_ROLE_ID}}") # Assuming Super Admin's user ID is 1
print_response $? "$RESPONSE"

# Test 6: Get all roles
echo -e "\nGetting all roles..."
RESPONSE=$(curl -s -X GET "$BASE_URL/roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
print_response $? "$RESPONSE"

# Test 7: Get all permissions
echo -e "\nGetting all permissions..."
RESPONSE=$(curl -s -X GET "$BASE_URL/permissions/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
print_response $? "$RESPONSE"
