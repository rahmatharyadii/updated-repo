#!/usr/bin/env python3
"""
GitHub Contributions Generator Web UI (Preview Mode)
"""

import os
import subprocess
from datetime import datetime, timedelta
import random
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GitHub Contributions</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f6f8fa; margin: 40px; }
        .container { background: white; padding: 20px 30px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
        label { font-weight: 600; display: block; margin-top: 15px; margin-bottom: 5px; font-size: 14px; }
        input[type="date"], input[type="number"] { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #d1d5da; border-radius: 4px; font-size: 14px; }
        input:focus { border-color: #0366d6; outline: none; box-shadow: 0 0 0 3px rgba(3,102,214,0.3); }
        button { background: #2ea44f; color: white; border: none; padding: 10px 15px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 25px; font-weight: 500; }
        button:hover { background: #2c974b; }
        button:disabled { background: #94d3a2; cursor: not-allowed; }
        button.secondary { background: #0366d6; margin-top: 20px; }
        button.secondary:hover { background: #005cc5; }
        button.secondary:disabled { background: #79b8ff; }
        button.delBtn { background: #cb2431; margin-top: 0; padding: 6px 12px; width: auto; font-size: 14px; }
        button.delBtn:hover { background: #9e1c23; }
        
        #log { margin-top: 15px; font-size: 14px; color: #586069; text-align: center; font-weight: 500; }
        .success { color: #2ea44f !important; }
        .error { color: #cb2431 !important; }
        
        /* Table Styles */
        #planSection { display: none; margin-top: 30px; border-top: 2px solid #eaecef; padding-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
        th, td { border: 1px solid #dfe2e5; padding: 8px 12px; text-align: center; }
        th { background-color: #f6f8fa; }
        td input { text-align: center; }
        .day-name { font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="margin-top:0; text-align: center; color: #24292e;">🚀 Git Contributions</h2>
        
        <!-- Step 1: Settings Form -->
        <form id="genForm">
            <label>Start Date</label>
            <input type="date" id="startDate" value="2021-11-15" required>
            
            <label>End Date</label>
            <input type="date" id="endDate" value="2021-12-30" required>
            
            <label>Min Commits/day</label>
            <input type="number" id="minC" value="1" min="0" required>
            
            <label>Max Commits/day</label>
            <input type="number" id="maxC" value="15" min="0" required>
            
            <button type="submit">Preview Rencana Commit</button>
        </form>

        <!-- Step 2: The Generated Plan -->
        <div id="planSection">
            <h3 style="margin-bottom:0px;color:#24292e;">📝 Rencana Konfigurasi Commit</h3>
            <p style="font-size:13px; color:#586069; margin-top:5px;">Anda bisa mengubah jumlah commit atau menghapus baris di bawah ini sebelum mengeksekusinya ke dalam git.</p>
            
            <form id="executeForm">
                <table>
                    <thead>
                        <tr>
                            <th>Tanggal</th>
                            <th>Hari</th>
                            <th style="width: 120px;">Jumlah Commit</th>
                            <th style="width: 70px;">Aksi</th>
                        </tr>
                    </thead>
                    <tbody id="planBody">
                    </tbody>
                </table>
                <button type="submit" class="secondary" id="execBtn">Eksekusi Commits Sekarang!</button>
            </form>
        </div>

        <div id="log"></div>
    </div>
    
    <script>
        const daysIndo = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
        
        // Set default dates to today
        const todayStr = new Date();
        // Shift timezone so toISOString gives local date properly
        const localDate = new Date(todayStr.getTime() - (todayStr.getTimezoneOffset() * 60000)).toISOString().split('T')[0];
        document.getElementById('startDate').value = localDate;
        document.getElementById('endDate').value = localDate;
        
        // Random number logic
        function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

        // Handle step 1 (Preview Plan)
        document.getElementById('genForm').onsubmit = (e) => {
            e.preventDefault();
            
            const startStr = document.getElementById('startDate').value;
            const endStr = document.getElementById('endDate').value;
            const start = new Date(startStr);
            const end = new Date(endStr);
            const minC = parseInt(document.getElementById('minC').value);
            const maxC = parseInt(document.getElementById('maxC').value);
            
            if (start > end) {
                alert("Start Date tidak boleh lebih besar dari End Date!");
                return;
            }
            if (minC > maxC) {
                alert("Min Commits tidak boleh lebih besar dari Max Commits!");
                return;
            }

            const tbody = document.getElementById('planBody');
            tbody.innerHTML = '';
            
            // Loop from start to end date
            let current = new Date(startStr);
            while (current <= end) {
                const dateStr = current.toISOString().split('T')[0];
                const dayName = daysIndo[current.getDay()];
                const commits = getRandomInt(minC, maxC);
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${dateStr}</td>
                    <td class="day-name">${dayName}</td>
                    <td>
                        <input type="number" value="${commits}" min="0">
                    </td>
                    <td>
                        <button type="button" class="delBtn" onclick="this.closest('tr').remove()" title="Hapus hari ini dari rencana">Hapus</button>
                    </td>
                `;
                tbody.appendChild(tr);
                
                // Add 1 day
                current.setDate(current.getDate() + 1);
            }
            
            document.getElementById('planSection').style.display = 'block';
            document.getElementById('log').textContent = '';
            document.getElementById('log').className = '';
        };

        // Handle step 2 (Execute Commits)
        document.getElementById('executeForm').onsubmit = async (e) => {
            e.preventDefault();
            
            const btn = document.getElementById('execBtn');
            const log = document.getElementById('log');
            btn.disabled = true;
            btn.textContent = 'Mengeksekusi... (Bisa butuh beberapa menit)';
            log.textContent = 'Memproses commit di latar belakang...';
            log.className = '';
            
            // Collect the edited plan
            const payload = [];
            const tbody = document.getElementById('planBody');
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(row => {
                const dateStr = row.cells[0].textContent;
                const commitsInput = row.cells[2].querySelector('input').value;
                const commitsCount = parseInt(commitsInput) || 0;
                
                if (commitsCount > 0) {
                    payload.push({ date: dateStr, commits: commitsCount });
                }
            });

            try {
                const res = await fetch('/execute', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (res.ok) {
                    log.textContent = data.message;
                    log.className = 'success';
                } else {
                    log.textContent = 'Gagal: ' + data.error;
                    log.className = 'error';
                }
            } catch (err) {
                log.textContent = 'Terjadi kesalahan: ' + err;
                log.className = 'error';
            }
            
            btn.disabled = false;
            btn.textContent = 'Eksekusi Commits Sekarang!';
        };
    </script>
</body>
</html>
"""

def create_commit(date, commit_num):
    filename = "contributions.txt"
    with open(filename, "a") as f:
        f.write(f"Contribution on {date} - Commit #{commit_num}\n")
    
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date
    env['GIT_COMMITTER_DATE'] = date
    
    subprocess.run(['git', 'add', filename], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['git', 'commit', '-m', f'Contribution: {date}'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
        
    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                plan = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode('utf-8'))
                return
                
            commit_count = 0
            for item in plan:
                try:
                    date_str = item.get('date')
                    commits = item.get('commits', 0)
                    if commits <= 0:
                        continue
                        
                    for j in range(commits):
                        # Format: YYYY-MM-DDTHH:MM:SS
                        git_date = f"{date_str}T{12 + (j % 12):02d}:00:00"
                        create_commit(git_date, commit_count + 1)
                        commit_count += 1
                except Exception as e:
                    pass
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                "message": f"✅ Berhasil! {commit_count} commits telah dieksekusi. (Jalankan 'git push origin main' di terminal Anda)"
            }).encode('utf-8'))

def main():
    if not os.path.exists('.git'):
        print("❌ Bukan repository git! Silakan jalankan 'git init' terlebih dahulu.")
        return
        
    port = 8080
    server_address = ('', port)
    
    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError as e:
        port = 8081
        server_address = ('', port)
        try:
            httpd = HTTPServer(server_address, RequestHandler)
        except OSError as e:
            port = 8082
            server_address = ('', port)
            try:
                httpd = HTTPServer(server_address, RequestHandler)
            except OSError as e:
                port = 8083
                server_address = ('', port)
                httpd = HTTPServer(server_address, RequestHandler)

    print(f"✅ Web UI berjalan di http://localhost:{port}")
    print("Membuka browser otomatis...")
    webbrowser.open(f'http://localhost:{port}')
    
    print("Tekan Ctrl+C untuk menghentikan server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nMenghentikan server...")
    httpd.server_close()

if __name__ == "__main__":
    main()
