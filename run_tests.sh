#!/bin/bash

# Exit ngay nếu có lỗi
set -e

# === 1. Kích hoạt virtualenv ===
# Giả sử venv tên .venv (bạn có thể đổi nếu tên khác)
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found! Please create and try again."
    exit 1
fi

# === 2. Chạy test suite với pytest ===
echo "🚀 Running test suite..."
pytest tests/ -v
test_exit_code=$?

# === 3. Trả về exit code cho CI ===
if [ $test_exit_code -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
