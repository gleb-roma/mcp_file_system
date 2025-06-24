#!/usr/bin/env python3
"""
Simple test script for the MCP File System Server
"""
import asyncio
import tempfile
import os
from pathlib import Path
from main import read_file, write_file, list_directory, delete_file, move_file, copy_file

async def test_file_operations():
    """Test all file operations"""
    print("🧪 Testing MCP File System Server...")
    
    # Test write_file
    print("\n1. Testing write_file...")
    result = await write_file("test.txt", "Hello, MCP!")
    print(f"   Result: {result}")
    
    # Test read_file
    print("\n2. Testing read_file...")
    result = await read_file("test.txt")
    print(f"   Result: {result}")
    
    # Test list_directory
    print("\n3. Testing list_directory...")
    result = await list_directory(".")
    print(f"   Result: {result}")
    
    # Test copy_file
    print("\n4. Testing copy_file...")
    result = await copy_file("test.txt", "test_copy.txt")
    print(f"   Result: {result}")
    
    # Test move_file
    print("\n5. Testing move_file...")
    result = await move_file("test_copy.txt", "test_moved.txt")
    print(f"   Result: {result}")
    
    # Test delete_file
    print("\n6. Testing delete_file...")
    result = await delete_file("test_moved.txt")
    print(f"   Result: {result}")
    
    # Clean up
    print("\n7. Cleaning up...")
    try:
        await delete_file("test.txt")
        print("   Cleanup successful")
    except:
        pass
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_file_operations()) 