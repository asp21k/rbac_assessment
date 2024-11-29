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
    -d '{"email":"superadmin@example.com","password":"SuperAdmin123!"}')
ACCESS_TOKEN=$(echo $RESPONSE | python -m json.tool | grep access | cut -d '"' -f 4)
print_response $? "$RESPONSE"

# Test 2: Get all users
echo -e "\nGetting all users..."
RESPONSE=$(curl -s -X GET "$BASE_URL/users/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
print_response $? "$RESPONSE"

# Test 3: Create new role
echo -e "\nCreating new role..."
RESPONSE=$(curl -s -X POST "$BASE_URL/roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Test Role","description":"Test role description","permission_ids":[1]}')
print_response $? "$RESPONSE"

# Test 4: Get all roles
echo -e "\nGetting all roles..."
RESPONSE=$(curl -s -X GET "$BASE_URL/roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
print_response $? "$RESPONSE"

# Test 5: Create new user
echo -e "\nCreating new user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
    -H "Content-Type: application/json" \
    -d '{"email":"newuser@example.com","username":"newuser","password":"NewUser123!","first_name":"New","last_name":"User"}')
print_response $? "$RESPONSE"

# Test 6: Assign role to user
echo -e "\nAssigning role to user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/user-roles/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"user":5,"role":2}')
print_response $? "$RESPONSE"

# Test 7: Get all permissions
echo -e "\nGetting all permissions..."
RESPONSE=$(curl -s -X GET "$BASE_URL/permissions/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
print_response $? "$RESPONSE"