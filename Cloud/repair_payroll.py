import os

def fix_payroll():
    path = 'e:/proj/pnchs/pages/payroll.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the corrupted section
    start_tag = '<!-- ── Payslip Modal ── -->'
    start_idx = content.find(start_tag)
    if start_idx == -1:
        print("Start tag not found")
        return

    new_content = """  <!-- ── Payslip Modal ── -->
  <div class="modal-overlay" id="payslipModal" style="z-index:3000;">
    <div id="payslipContent" style="position:relative; width: 850px; max-height:88vh; overflow-y:auto; border-radius:14px; box-shadow:0 24px 60px rgba(0,0,0,0.22); font-family: 'Courier New', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 35px 25px 25px; box-sizing: border-box; text-transform: uppercase;">
      
      <div id="payslipHeaderControls" style="position:absolute;top:20px;right:25px;display:flex;gap:8px; z-index: 50; font-family: sans-serif; font-weight: bold; text-transform: none;">
        <button onclick="printAdminPayslip()" style="background:#f1f5f9;border:1px solid #cbd5e1;border-radius:7px;padding:6px 12px;color:#0f172a;font-size:11px;cursor:pointer;display:flex;align-items:center;gap:5px;">
            Print
        </button>
        <button id="closePayslip" style="background:#fee2e2;border:1px solid #fecaca;border-radius:7px;padding:6px 12px;color:#991b1b;font-size:11px;cursor:pointer;">&times; Close</button>
      </div>

      <div style="display: flex; justify-content: space-between; margin-bottom: 25px;">
        <div style="flex: 1;" id="ps_print_date"></div>
        <div style="text-align: center; flex: 2; line-height: 1.5;">
          Republic of the Philippines<br>
          DEPARTMENT OF EDUCATION<br>
          OFFICIAL PAYROLL SLIP
        </div>
        <div style="text-align: right; flex: 1;">
          <span id="ps_print_id">000000</span>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; padding-bottom: 5px; margin-bottom: 10px;">
        <div id="ps_issue_date" style="flex: 1;"></div>
        <div id="ps_month_label" style="text-align: center; flex: 2;">For the Month of ...</div>
        <div style="text-align: right; flex: 1;">Page 1 Of 1</div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; border-bottom: 1px dashed #000; padding-bottom: 15px; margin-bottom: 10px;">
        <div style="padding-right: 10px;">
          <div style="margin-bottom:2px;">Name: <span id="ps_name"></span></div>
          <div style="display: flex; justify-content: space-between; margin-bottom:2px;">
            <span>Employee No.: <span id="ps_id"></span></span>
            <span>Account No.: ----------</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom:2px;">
            <span>Date of Hiring: &nbsp;/ &nbsp;/</span>
            <span>Date of Retirement:</span>
          </div>
          <div style="margin-bottom:2px;">Position: <span id="ps_designation"></span></div>
          <div style="bottom:2px;">Grade: -- &nbsp;&nbsp;Step: -</div>
          <div style="margin-bottom:2px;">Tax Code: S Single/Married</div>
          <div>Amount of Exemption:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0</div>
        </div>
        <div style="padding-left: 20px;">
          <div style="margin-bottom:2px;">Reg: 06 REGION VI - WESTERN VISAYAS</div>
          <div style="margin-bottom:2px;">Div: 022 ILOILO</div>
          <div style="margin-bottom:2px;">Sta: 500 SENIOR HIGH SCHOOL</div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px; margin-bottom:2px;">
            <span>Basic Salary:</span><span id="ps_basic_full"></span>
          </div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px; margin-bottom:12px;">
            <span>P.E.R.A.:</span><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.00</span>
          </div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px;">
            <span>Gross Compensation:</span><span id="ps_gross"></span>
          </div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; border-bottom: 1px dashed #000; padding-bottom: 5px; margin-bottom: 5px;">
        <div style="text-align: center; letter-spacing: 5px;">D E D U C T I O N S</div>
        <div style="text-align: center; letter-spacing: 2px;">UNDEDUCTED OBLIGATIONS</div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; margin-bottom: 10px; min-height: 180px;">
        <div style="padding-right: 15px; border-right: 1px dashed #000;">
          <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; margin-bottom: 5px; padding-bottom: 5px;">
            <span style="flex: 2;">Deduction<br>Code Description</span>
            <span style="display:flex; flex: 2; gap: 10px; text-align: right;">
              <span style="width: 70px;">Effectivity<br>Date</span>
              <span style="width: 75px;">Termination<br>Date</span>
              <span style="width: 75px;">Amount Of<br>Deduction</span>
            </span>
          </div>
          <div id="ps_deductions_list" style="margin-bottom: 15px;"></div>
          <div style="display: flex; justify-content: space-between; border-top: 1px dashed #000; padding-top: 10px;">
            <span>Total Deductions:</span>
            <span id="ps_total_deduct" style="padding-right: 5px;"></span>
          </div>
        </div>
        <div style="padding-left: 15px;">
           <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; margin-bottom: 5px; padding-bottom: 5px;">
            <span style="flex: 2;">Deduction<br>Code Description</span>
            <span style="display:flex; flex: 2; gap: 5px; text-align: right;">
              <span style="width: 60px;">Effect<br>Date</span>
              <span style="width: 60px;">Termin<br>Date</span>
              <span style="width: 75px;">Amount Of<br>Deduction</span>
            </span>
          </div>
        </div>
      </div>

      <div style="border-bottom: 1px dashed #000; padding-bottom: 15px; margin-bottom: 15px;">
        <div style="display: flex; width: 380px; justify-content: space-between; margin-bottom: 5px;">
          <span style="letter-spacing: 2px;">N e t  P a y    :</span><span id="ps_net" style="padding-right: 5px;"></span>
        </div>
        <div style="display: flex; width: 380px; justify-content: space-between; margin-bottom: 5px;">
          <span>1st Half Pay :</span><span id="ps_half_net1" style="padding-right: 5px;"></span>
        </div>
        <div style="display: flex; width: 380px; justify-content: space-between;">
          <span>2nd Half Pay :</span><span id="ps_half_net2" style="padding-right: 5px;"></span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; gap: 30px;">
        <div style="border: 1px dashed #ccc; padding: 15px; height: 160px; position: relative;">
          <div style="text-align: center; margin-bottom: 10px;">Monthly Takehome Pay Chart</div>
          <div style="position:absolute; left:50px; top: 40px; bottom: 30px; border-left: 1px solid #000;"></div>
          <div style="position:absolute; left:50px; bottom: 30px; right: 20px; border-bottom: 1px solid #000;"></div>
          <div style="position:absolute; bottom: 10px; left: 60px; display: flex; justify-content: space-between; right: 20px;">
            <span>F</span><span>M</span><span>A</span><span>M</span><span>J</span><span>J</span><span>A</span><span>S</span><span>O</span><span>N</span><span>D</span><span>J</span>
          </div>
          <div style="position:absolute; left: 5px; bottom: 30px; display:flex; flex-direction:column; justify-content: space-between; top: 40px; padding-right: 5px; text-align: right;">
            <span>12000</span><span>9000</span><span>6000</span><span>3000</span>
          </div>
        </div>
        <div style="border: 1px dashed #000; padding: 12px;">
          <div style="text-align: center; border-bottom: 1px dashed #000; padding-bottom: 8px; margin-bottom: 15px;">NEW OBLIGATIONS<br>(To be filled up by GFI/PLI)</div>
          <div style="margin-bottom: 12px;">ORGANIZATION:</div>
          <div style="margin-bottom: 12px;">TYPE:</div>
          <div style="margin-bottom: 12px;">AMOUNT LOANED:</div>
          <div style="margin-bottom: 12px;">MONTHLY AMORTIZATION:</div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  (function () {
    const API_PROCESS = '/api/payroll/process';
    const API_RUNS = '/api/payroll/runs';
    let payrollData = null;
    let records = [];
    let activeKey = null;
    let activeTab = 'all';

    function fmt(n) { return '₱' + parseFloat(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
    function pad(str, len) { str = String(str); while (str.length < len) str = '&nbsp;' + str; return str; }
    function padRight(str, len) { str = String(str); while (str.length < len) str = str + '&nbsp;'; return str; }

    async function loadRuns() {
      try {
        const res = await $.get(API_RUNS);
        records = res;
        renderDocList();
        if (records.length > 0 && !activeKey) {
          selectRecord(records[0].key);
        } else if (activeKey && records.find(r => r.key === activeKey)) {
          selectRecord(activeKey);
        } else if (records.length > 0) {
          selectRecord(records[0].key);
        } else {
          $('#prDetail').removeClass('visible');
          $('#prEmpty').show();
        }
      } catch (e) { console.error('Failed to load runs', e); }
    }

    async function selectRecord(key) {
      const rec = records.find(r => r.key === key);
      if (!rec) return;
      activeKey = key;
      renderDocList();
      $('#prEmpty').hide();
      if (!rec.data) {
        $('#pageHeaderTitle').text('Loading...');
        try {
          rec.data = await $.get(API_PROCESS, { year: rec.year, month: rec.month, half: rec.half });
        } catch (e) { console.error(e); return; }
      }
      payrollData = rec.data;
      renderDetail(rec);
    }

    function renderDocList() {
      const filtered = activeTab === 'all' ? records
        : records.filter(r => r.status.toLowerCase() === activeTab);

      if (!filtered.length) {
        $('#docList').html('<div style="padding:20px 18px;font-size:12px;color:var(--muted2);">No records found.</div>');
        return;
      }

      const sColors = { draft: '#92400e', 'for approval': '#0284c7', approved: 'var(--green)', rejected: 'var(--red)' };
      const sBgs = { draft: '#fef3c7', 'for approval': '#e0f2fe', approved: 'var(--green-dim)', rejected: 'var(--red-dim)' };

      $('#docList').html(filtered.map(r => `
      <div class="doc-row${r.key === activeKey ? ' active' : ''}" data-key="${r.key}">
        <div class="doc-period">${r.period}</div>
        <div class="doc-meta">
          <span>Faculty Payroll</span>
          <span class="dtr-pill" style="background:${sBgs[r.status.toLowerCase()]};color:${sColors[r.status.toLowerCase()]};">${r.status}</span>
        </div>
      </div>
    `).join(''));

      $('#docList .doc-row').on('click', function () {
        selectRecord($(this).data('key'));
      });
    }

    function renderDetail(rec) {
      const data = rec.data;
      $('#prDetail').addClass('visible');
      $('#pageHeaderTitle').text(data.period);

      if (rec.remarks && rec.status === 'Rejected') {
        $('#pageHeaderRemarks').text('Rejected: ' + rec.remarks).show();
      } else {
        $('#pageHeaderRemarks').hide();
      }

      $('#sumGross').text(fmt(data.summary.grand_total_gross));
      $('#sumDeduct').text(fmt(data.summary.grand_total_deduct));
      $('#sumNet').text(fmt(data.summary.grand_total_net));
      $('#sumCreatedAt').text(data.created_at || '—');

      if (rec.status === 'Draft' || rec.status === 'Rejected') {
          $('#btnSendApproval').show().text('Send for Approval').prop('disabled', false).css('opacity', '1');
          $('#btnDeletePayroll').show();
      } else {
          $('#btnSendApproval').show().text('✓ ' + rec.status).prop('disabled', true).css('opacity', '0.55');
          $('#btnDeletePayroll').hide();
      }

      const rows = data.employees.map(e => `
      <tr onclick="showEmp('${e.id}')" style="cursor:pointer;">
        <td><strong>${e.name}</strong><br><small style="color:var(--muted2)">${e.id}</small></td>
        <td>${e.designation}</td>
        <td class="num">${e.late_minutes}m late${e.undertime_minutes ? ' / ' + e.undertime_minutes + 'm under' : ''}</td>
        <td class="num">${e.dtr_filed ? '<span class="dtr-pill full">OK</span>' : '<span class="dtr-pill absent">NO LOGS</span>'}</td>
        <td class="num amt-earn">${fmt(e.total_gross)}</td>
        <td class="num amt-deduct">${fmt(e.total_deduct)}</td>
        <td class="num amt-net">${fmt(e.net_pay)}</td>
        <td style="text-align:center;">
          <button onclick="event.stopPropagation();showPayslip('${e.id}')" title="View Payslip"
            style="background:var(--navy-light);border:1.5px solid #c5d8f5;border-radius:7px;padding:5px 10px;cursor:pointer;color:var(--navy-mid);font-size:11px;font-weight:600;display:inline-flex;align-items:center;gap:4px;transition:all .15s;" onmouseover="this.style.background='var(--navy)';this.style.color='#fff'" onmouseout="this.style.background='var(--navy-light)';this.style.color='var(--navy-mid)'">
            <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            Payslip
          </button>
        </td>
        <td><svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></td>
      </tr>
    `).join('');
      $('#payrollTableBody').html(rows);
    }

    window.currentViewedEmpId = null;
    window.showEmp = function (id) {
      if (!payrollData) return;
      const e = payrollData.employees.find(x => x.id === id);
      if (!e) return;
      window.currentViewedEmpId = id;
      const runRec = records.find(r => r.key === activeKey);
      const isDraft = (runRec && (runRec.status === 'Draft' || runRec.status === 'Rejected'));
      
      $('#drawerName').text(e.name);
      if (isDraft) {
        $('#earningList').html(`
          <div class="ph-row"><span>Basic Salary (50%)</span><input type="number" step="0.01" id="eHalfBasic" value="${e.half_basic}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;"></div>
          <div class="ph-row"><span>Other Earnings</span><input type="number" step="0.01" id="eOtherEarn" value="${e.other_earnings || 0}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;"></div>
        `);
        $('#deductList').html(`
          <div class="ph-row"><span>Static Deductions</span><input type="number" step="0.01" id="eOtherDeduct" value="${e.other_deductions || 0}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;"></div>
          <div class="ph-row"><span>Absence Deduction</span><input type="number" step="0.01" id="eAbsentDeduct" value="${e.absent_deduction}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;color:var(--red)"></div>
          <div class="ph-row"><span>Tardiness Deduction</span><input type="number" step="0.01" id="eLateDeduct" value="${e.tardiness_deduction}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;color:var(--red)"></div>
          <div class="ph-row"><span>Undertime Deduction</span><input type="number" step="0.01" id="eUndertimeDeduct" value="${e.undertime_deduction || 0}" style="background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:4px 8px;width:105px;text-align:right;font-size:12px;color:var(--red)"></div>
          <div style="margin-top:16px;"><button class="btn btn-primary" style="width:100%;justify-content:center;font-size:12px;padding:9px;" onclick="saveEmpDetails()">Save Adjustments</button></div>
        `);
      } else {
        $('#earningList').html(`<div class="ph-row"><input value="Basic Salary (50%)" readonly><input value="${fmt(e.half_basic)}" readonly></div>`);
        $('#deductList').html(`
          <div class="ph-row"><input value="Static Deductions" readonly><input value="${fmt(e.other_deductions)}" readonly></div>
          <div class="ph-row"><input value="Absence Deduction" readonly><input value="${fmt(e.absent_deduction)}" style="color:var(--red)" readonly></div>
          <div class="ph-row"><input value="Tardiness (${e.late_minutes} min)" readonly><input value="${fmt(e.tardiness_deduction)}" style="color:var(--red)" readonly></div>
          <div class="ph-row"><input value="Undertime (${e.undertime_minutes || 0} min)" readonly><input value="${fmt(e.undertime_deduction || 0)}" style="color:var(--red)" readonly></div>
        `);
      }
      $('#dGross').text(fmt(e.total_gross));
      $('#dDeduct').text(fmt(e.total_deduct));
      $('#dNet').text(fmt(e.net_pay));
      $('#payheadDrawer').addClass('open');
    };

    window.saveEmpDetails = async function () {
      if (!window.currentViewedEmpId || !activeKey) return;
      const payload = {
        half_basic: $('#eHalfBasic').val(),
        other_earnings: $('#eOtherEarn').val(),
        other_deductions: $('#eOtherDeduct').val(),
        absent_deduction: $('#eAbsentDeduct').val(),
        tardiness_deduction: $('#eLateDeduct').val(),
        undertime_deduction: $('#eUndertimeDeduct').val()
      };
      const btn = $('#deductList button');
      btn.prop('disabled', true).text('Saving...');
      try {
        const res = await fetch(API_RUNS + '/' + activeKey + '/details/' + window.currentViewedEmpId, {
          method: 'PUT', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.error) { alert(data.error); btn.prop('disabled', false).text('Save Adjustments'); return; }
        const rec = records.find(r => r.key === activeKey);
        rec.data = await $.get(API_PROCESS, { year: rec.year, month: rec.month, half: rec.half });
        payrollData = rec.data;
        renderDetail(rec);
        showEmp(window.currentViewedEmpId);
      } catch (e) { alert('Error updating properties'); console.error(e); btn.prop('disabled', false).text('Save Adjustments'); }
    };

    window.showPayslip = function (id) {
      if (!payrollData) return;
      const e = payrollData.employees.find(x => x.id === id);
      if (!e) return;
      $('#ps_name').text(e.name);
      $('#ps_id').text(e.id);
      $('#ps_designation').text(e.designation);
      const pD = new Date();
      $('#ps_print_date').html(pD.toLocaleDateString('en-US') + '<br>' + pD.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }));
      $('#ps_issue_date').text(pD.toLocaleDateString('en-US'));
      $('#ps_month_label').text(`For the Period of ${payrollData.period}`);
      const rId = Math.floor(Math.random() * 900000) + 100000;
      $('#ps_print_id').text(rId);
      $('#ps_basic_full').html(pad(fmt(e.basic_salary).replace('₱', ''), 14));
      $('#ps_gross').html(pad(fmt(e.total_gross).replace('₱', ''), 14));
      let dhtml = [];
      const addD = (c, d, a) => {
        if (!a || parseFloat(a) === 0) return;
        dhtml.push(`<div style="display:flex; justify-content: space-between; margin-bottom:3px;"><span style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 5px;">${padRight(c, 4)} ${d}</span><span style="display:flex; flex: 2; gap: 10px; text-align: right;"><span style="width: 70px;">--</span><span style="width: 75px;">--</span><span style="width: 75px;">${pad(fmt(a).replace('₱', ''), 10)}</span></span></div>`);
      };
      addD('ABS', 'ABSENCE', e.absent_deduction);
      addD('TRD', 'TARDINESS', e.tardiness_deduction);
      addD('UND', 'UNDERTIME', e.undertime_deduction);
      addD('SSS', 'SSS PREMIUM', e.sss_ee);
      addD('PHIC', 'PHILHEALTH', e.philhealth_ee);
      addD('HDMF', 'PAG-IBIG FUND', e.pagibig_ee);
      addD('BIR', 'WITHHOLDING TAX', e.withholding_tax);
      addD('OTH', 'OTHER DEDUCTIONS', e.other_deductions);
      $('#ps_deductions_list').html(dhtml.join(''));
      $('#ps_total_deduct').html(pad(fmt(e.total_deduct).replace('₱', ''), 14));
      $('#ps_net').html(pad(fmt(e.net_pay).replace('₱', ''), 14));
      const h1 = Math.floor(e.net_pay / 2 * 100) / 100;
      const h2 = (e.net_pay - h1).toFixed(2);
      $('#ps_half_net1').html(pad(fmt(h1).replace('₱', ''), 14));
      $('#ps_half_net2').html(pad(fmt(h2).replace('₱', ''), 14));
      $('#payslipModal').addClass('open');
    };

    window.printAdminPayslip = function () {
      const prt = document.getElementById("payslipContent");
      const ctrl = document.getElementById("payslipHeaderControls");
      if (ctrl) ctrl.style.display = 'none';
      const WinPrint = window.open('', '', 'left=0,top=0,width=850,height=900,toolbar=0,scrollbars=0,status=0');
      WinPrint.document.write('<html><head><style>@page { size: portrait; margin: 10mm; } body { background: #fff; line-height: 1.35; -webkit-print-color-adjust: exact; }</style></head><body>');
      WinPrint.document.write(prt.outerHTML.replace('max-height:88vh', 'max-height:none').replace('overflow-y:auto', 'overflow:visible'));
      WinPrint.document.write('</body></html>');
      WinPrint.document.close();
      WinPrint.focus();
      setTimeout(() => { WinPrint.print(); WinPrint.close(); if (ctrl) ctrl.style.display = 'flex'; }, 500);
    };

    $('#closePayslip').on('click', () => $('#payslipModal').removeClass('open'));
    $('#payslipModal').on('click', function (e) { if (e.target === this) $(this).removeClass('open'); });
    $('#hideDrawer').on('click', () => $('#payheadDrawer').removeClass('open'));
    $('.ftab').on('click', function () { $('.ftab').removeClass('active'); $(this).addClass('active'); activeTab = $(this).text().trim().toLowerCase(); renderDocList(); });

    $('#btnSendApproval').on('click', async function () {
      if (!confirm('Are you sure you want to send this payroll for approval?')) return;
      try {
        await fetch(API_RUNS + '/' + activeKey + '/status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: 'For Approval' }) });
        loadRuns();
      } catch (e) { alert('Error updating status.'); }
    });

    $('#btnDeletePayroll').on('click', async function () {
      if (!confirm('Are you certain you wish to delete this payroll?')) return;
      try {
        await fetch(API_RUNS + '/' + activeKey, { method: 'DELETE' });
        activeKey = null;
        loadRuns();
      } catch (e) { alert('Error deleting record.'); }
    });

    (function () {
      const curY = new Date().getFullYear();
      const $sel = $('#npYear').empty();
      for (let y = curY - 1; y <= curY + 2; y++) {
        $sel.append(`<option value="${y}"${y === curY ? ' selected' : ''}>${y}</option>`);
      }
    })();

    $('#btnNewDoc').on('click', function () {
      $('#npError').hide();
      $('#confirmNewPayroll').prop('disabled', false).html('<svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg> Generate Payroll');
      $('#newPayrollModal').addClass('open');
    });

    $('#cancelNewPayroll').on('click', () => $('#newPayrollModal').removeClass('open'));
    $('#newPayrollModal').on('click', function (e) { if (e.target === this) $(this).removeClass('open'); });

    $('#confirmNewPayroll').on('click', async function () {
      const y = $('#npYear').val(), m = $('#npMonth').val(), h = $('input[name="npHalf"]:checked').val(), key = `${y}-${m}-${h}`;
      if (records.find(r => r.key === key)) { $('#npError').text('A payroll record for this period already exists.').show(); return; }
      $(this).prop('disabled', true).html('<span style="opacity:.6;">Generating…</span>');
      try {
        const res = await fetch(API_RUNS, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ year: parseInt(y), month: parseInt(m), half: parseInt(h) }) });
        const resD = await res.json();
        if (res.status !== 200) { $('#npError').text(resD.error).show(); $(this).prop('disabled', false).html('Generate Payroll'); return; }
        activeKey = resD.key; $('#newPayrollModal').removeClass('open'); await loadRuns();
      } catch (err) { alert('Failed to create payroll run.'); $(this).prop('disabled', false).html('Generate Payroll'); }
    });

    loadRuns();
  })();
</script>"""
    
    # We replace from start_idx to the end of the file
    content = content[:start_idx] + new_content
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("payroll.html fixed")

def fix_payroll_approval():
    path = 'e:/proj/pnchs/pages/payroll_approval.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the corrupted section
    start_tag = '<!-- ── Payslip Modal ── -->'
    start_idx = content.find(start_tag)
    if start_idx == -1:
        print("Start tag not found in approval")
        return

    new_content = """  <!-- ── Payslip Modal ── -->
  <div class="modal-overlay" id="payslipModal" style="z-index:3000;">
    <div id="payslipContent" style="position:relative; width: 850px; max-height:88vh; overflow-y:auto; border-radius:14px; box-shadow:0 24px 60px rgba(0,0,0,0.22); font-family: 'Courier New', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 35px 25px 25px; box-sizing: border-box; text-transform: uppercase;">
      
      <div id="payslipHeaderControls" style="position:absolute;top:20px;right:25px;display:flex;gap:8px; z-index: 50; font-family: sans-serif; font-weight: bold; text-transform: none;">
        <button onclick="printAdminPayslip()" style="background:#f1f5f9;border:1px solid #cbd5e1;border-radius:7px;padding:6px 12px;color:#0f172a;font-size:11px;cursor:pointer;display:flex;align-items:center;gap:5px;">
            Print
        </button>
        <button id="closePayslip" style="background:#fee2e2;border:1px solid #fecaca;border-radius:7px;padding:6px 12px;color:#991b1b;font-size:11px;cursor:pointer;">&times; Close</button>
      </div>

      <div style="display: flex; justify-content: space-between; margin-bottom: 25px;">
        <div style="flex: 1;" id="ps_print_date"></div>
        <div style="text-align: center; flex: 2; line-height: 1.5;">
          Republic of the Philippines<br>
          DEPARTMENT OF EDUCATION<br>
          OFFICIAL PAYROLL SLIP
        </div>
        <div style="text-align: right; flex: 1;">
          <span id="ps_print_id">000000</span>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; padding-bottom: 5px; margin-bottom: 10px;">
        <div id="ps_issue_date" style="flex: 1;"></div>
        <div id="ps_month_label" style="text-align: center; flex: 2;">For the Month of ...</div>
        <div style="text-align: right; flex: 1;">Page 1 Of 1</div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; border-bottom: 1px dashed #000; padding-bottom: 15px; margin-bottom: 10px;">
        <div style="padding-right: 10px;">
          <div style="margin-bottom:2px;">Name: <span id="ps_name"></span></div>
          <div style="display: flex; justify-content: space-between; margin-bottom:2px;">
            <span>Employee No.: <span id="ps_id"></span></span>
            <span>Account No.: ----------</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom:2px;">
            <span>Date of Hiring: &nbsp;/ &nbsp;/</span>
            <span>Date of Retirement:</span>
          </div>
          <div style="margin-bottom:2px;">Position: <span id="ps_designation"></span></div>
          <div style="margin-bottom:2px;">Grade: -- &nbsp;&nbsp;Step: -</div>
          <div style="margin-bottom:2px;">Tax Code: S Single/Married</div>
          <div>Amount of Exemption:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0</div>
        </div>
        <div style="padding-left: 20px;">
          <div style="margin-bottom:2px;">Reg: 06 REGION VI - WESTERN VISAYAS</div>
          <div style="margin-bottom:2px;">Div: 022 ILOILO</div>
          <div style="margin-bottom:2px;">Sta: 500 SENIOR HIGH SCHOOL</div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px; margin-bottom:2px;">
            <span>Basic Salary:</span><span id="ps_basic_full"></span>
          </div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px; margin-bottom:12px;">
            <span>P.E.R.A.:</span><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.00</span>
          </div>
          <div style="display: flex; justify-content: space-between; padding-left: 20px;">
            <span>Gross Compensation:</span><span id="ps_gross"></span>
          </div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; border-bottom: 1px dashed #000; padding-bottom: 5px; margin-bottom: 5px;">
        <div style="text-align: center; letter-spacing: 5px;">D E D U C T I O N S</div>
        <div style="text-align: center; letter-spacing: 2px;">UNDEDUCTED OBLIGATIONS</div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; margin-bottom: 10px; min-height: 180px;">
        <div style="padding-right: 15px; border-right: 1px dashed #000;">
          <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; margin-bottom: 5px; padding-bottom: 5px;">
            <span style="flex: 2;">Deduction<br>Code Description</span>
            <span style="display:flex; flex: 2; gap: 10px; text-align: right;">
              <span style="width: 70px;">Effectivity<br>Date</span>
              <span style="width: 75px;">Termination<br>Date</span>
              <span style="width: 75px;">Amount Of<br>Deduction</span>
            </span>
          </div>
          <div id="ps_deductions_list" style="margin-bottom: 15px;"></div>
          <div style="display: flex; justify-content: space-between; border-top: 1px dashed #000; padding-top: 10px;">
            <span>Total Deductions:</span>
            <span id="ps_total_deduct" style="padding-right: 5px;"></span>
          </div>
        </div>
        <div style="padding-left: 15px;">
           <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #000; margin-bottom: 5px; padding-bottom: 5px;">
            <span style="flex: 2;">Deduction<br>Code Description</span>
            <span style="display:flex; flex: 2; gap: 5px; text-align: right;">
              <span style="width: 60px;">Effect<br>Date</span>
              <span style="width: 60px;">Termin<br>Date</span>
              <span style="width: 75px;">Amount Of<br>Deduction</span>
            </span>
          </div>
        </div>
      </div>

      <div style="border-bottom: 1px dashed #000; padding-bottom: 15px; margin-bottom: 15px;">
        <div style="display: flex; width: 380px; justify-content: space-between; margin-bottom: 5px;">
          <span style="letter-spacing: 2px;">N e t  P a y    :</span><span id="ps_net" style="padding-right: 5px;"></span>
        </div>
        <div style="display: flex; width: 380px; justify-content: space-between; margin-bottom: 5px;">
          <span>1st Half Pay :</span><span id="ps_half_net1" style="padding-right: 5px;"></span>
        </div>
        <div style="display: flex; width: 380px; justify-content: space-between;">
          <span>2nd Half Pay :</span><span id="ps_half_net2" style="padding-right: 5px;"></span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 55% 45%; gap: 30px;">
        <div style="border: 1px dashed #ccc; padding: 15px; height: 160px; position: relative;">
          <div style="text-align: center; margin-bottom: 10px;">Monthly Takehome Pay Chart</div>
          <div style="position:absolute; left:50px; top: 40px; bottom: 30px; border-left: 1px solid #000;"></div>
          <div style="position:absolute; left:50px; bottom: 30px; right: 20px; border-bottom: 1px solid #000;"></div>
          <div style="position:absolute; bottom: 10px; left: 60px; display: flex; justify-content: space-between; right: 20px;">
            <span>F</span><span>M</span><span>A</span><span>M</span><span>J</span><span>J</span><span>A</span><span>S</span><span>O</span><span>N</span><span>D</span><span>J</span>
          </div>
          <div style="position:absolute; left: 5px; bottom: 30px; display:flex; flex-direction:column; justify-content: space-between; top: 40px; padding-right: 5px; text-align: right;">
            <span>12000</span><span>9000</span><span>6000</span><span>3000</span>
          </div>
        </div>
        <div style="border: 1px dashed #000; padding: 12px;">
          <div style="text-align: center; border-bottom: 1px dashed #000; padding-bottom: 8px; margin-bottom: 15px;">NEW OBLIGATIONS<br>(To be filled up by GFI/PLI)</div>
          <div style="margin-bottom: 12px;">ORGANIZATION:</div>
          <div style="margin-bottom: 12px;">TYPE:</div>
          <div style="margin-bottom: 12px;">AMOUNT LOANED:</div>
          <div style="margin-bottom: 12px;">MONTHLY AMORTIZATION:</div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  (function () {
    const API_PROCESS = '/api/payroll/process';
    const API_RUNS = '/api/payroll/runs';
    let payrollData = null;
    let records = [];
    let activeKey = null;
    let activeTab = 'all';

    function fmt(n) { return '₱' + parseFloat(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
    function pad(str, len) { str = String(str); while (str.length < len) str = '&nbsp;' + str; return str; }
    function padRight(str, len) { str = String(str); while (str.length < len) str = str + '&nbsp;'; return str; }

    async function loadRuns() {
      try {
        const res = await $.get(API_RUNS);
        records = res;
        renderDocList();
        if (records.length > 0 && !activeKey) {
          selectRecord(records[0].key);
        } else if (activeKey && records.find(r => r.key === activeKey)) {
          selectRecord(activeKey);
        } else if (records.length > 0) {
          selectRecord(records[0].key);
        } else {
          $('#prDetail').removeClass('visible');
          $('#prEmpty').show();
        }
      } catch (e) { console.error('Failed to load runs', e); }
    }

    async function selectRecord(key) {
      const rec = records.find(r => r.key === key);
      if (!rec) return;
      activeKey = key;
      renderDocList();
      $('#prEmpty').hide();
      if (!rec.data) {
        $('#pageHeaderTitle').text('Loading...');
        try {
          rec.data = await $.get(API_PROCESS, { year: rec.year, month: rec.month, half: rec.half });
        } catch (e) { console.error(e); return; }
      }
      payrollData = rec.data;
      renderDetail(rec);
    }

    function renderDocList() {
      const filtered = activeTab === 'all' ? records
        : records.filter(r => r.status.toLowerCase() === activeTab);

      if (!filtered.length) {
        $('#docList').html('<div style="padding:20px 18px;font-size:12px;color:var(--muted2);">No records found.</div>');
        return;
      }

      const sColors = { draft: '#92400e', 'for approval': '#0284c7', approved: 'var(--green)', rejected: 'var(--red)' };
      const sBgs = { draft: '#fef3c7', 'for approval': '#e0f2fe', approved: 'var(--green-dim)', rejected: 'var(--red-dim)' };

      $('#docList').html(filtered.map(r => `
      <div class="doc-row${r.key === activeKey ? ' active' : ''}" data-key="${r.key}">
        <div class="doc-period">${r.period}</div>
        <div class="doc-meta">
          <span>Faculty Payroll</span>
          <span class="dtr-pill" style="background:${sBgs[r.status.toLowerCase()]};color:${sColors[r.status.toLowerCase()]};">${r.status}</span>
        </div>
      </div>
    `).join(''));

      $('#docList .doc-row').on('click', function () {
        selectRecord($(this).data('key'));
      });
    }

    function renderDetail(rec) {
      const data = rec.data;
      $('#prDetail').addClass('visible');
      $('#pageHeaderTitle').text(data.period);
      
      if (rec.remarks && rec.status === 'Rejected') {
        $('#pageHeaderRemarks').text('Rejected: ' + rec.remarks).show();
      } else {
        $('#pageHeaderRemarks').hide();
      }

      $('#sumGross').text(fmt(data.summary.grand_total_gross));
      $('#sumDeduct').text(fmt(data.summary.grand_total_deduct));
      $('#sumNet').text(fmt(data.summary.grand_total_net));
      $('#sumCreatedAt').text(data.created_at || '—');

      $('#btnReject, #btnApprove, #lblStatus').hide();
      if (rec.status === 'For Approval') {
        $('#btnReject').show();
        $('#btnApprove').show();
      } else {
        const approvedMeta = (rec.status==='Approved' && rec.approved_by)
          ? `✓ ${rec.status} by ${rec.approved_by}${rec.approved_at ? ' · '+rec.approved_at : ''}`
          : rec.status;
        $('#lblStatus').show().text(approvedMeta)
          .css('background', rec.status==='Approved' ? 'var(--green-dim)' : 'var(--surface2)')
          .css('color', rec.status==='Approved' ? 'var(--green)' : 'var(--muted)');
      }

      const rows = data.employees.map(e => `
      <tr onclick="showEmp('${e.id}')" style="cursor:pointer;">
        <td><strong>${e.name}</strong><br><small style="color:var(--muted2)">${e.id}</small></td>
        <td>${e.designation}</td>
        <td class="num">${e.late_minutes}m late${e.undertime_minutes ? ' / '+e.undertime_minutes+'m under' : ''}</td>
        <td class="num">${e.dtr_filed ? '<span class="dtr-pill full">OK</span>' : '<span class="dtr-pill absent">NO LOGS</span>'}</td>
        <td class="num amt-earn">${fmt(e.total_gross)}</td>
        <td class="num amt-deduct">${fmt(e.total_deduct)}</td>
        <td class="num amt-net">${fmt(e.net_pay)}</td>
        <td style="text-align:center;">
          <button onclick="event.stopPropagation();showPayslip('${e.id}')" title="View Payslip"
            style="background:var(--navy-light);border:1.5px solid #c5d8f5;border-radius:7px;padding:5px 10px;cursor:pointer;color:var(--navy-mid);font-size:11px;font-weight:600;display:inline-flex;align-items:center;gap:4px;transition:all .15s;" onmouseover="this.style.background='var(--navy)';this.style.color='#fff'" onmouseout="this.style.background='var(--navy-light)';this.style.color='var(--navy-mid)'">
            <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            Payslip
          </button>
        </td>
        <td><svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></td>
      </tr>
    `).join('');
      $('#payrollTableBody').html(rows);
    }

    // ── Employee drawer ───────────────────────────────────────────────────────
    window.showEmp = function(id) {
      if (!payrollData) return;
      const e = payrollData.employees.find(x => x.id === id);
      if (!e) return;
      $('#drawerName').text(e.name);
      $('#earningList').html(`<div class="ph-row"><input value="Basic Salary (50%)" readonly><input value="${fmt(e.half_basic)}" readonly></div>`);
      $('#deductList').html(`
        <div class="ph-row"><input value="Static Deductions" readonly><input value="${fmt(e.other_deductions)}" readonly></div>
        <div class="ph-row"><input value="Absence Deduction" readonly><input value="${fmt(e.absent_deduction)}" style="color:var(--red)" readonly></div>
        <div class="ph-row"><input value="Tardiness (${e.late_minutes || 0} min)" readonly><input value="${fmt(e.tardiness_deduction)}" style="color:var(--red)" readonly></div>
        <div class="ph-row"><input value="Undertime (${e.undertime_minutes || 0} min)" readonly><input value="${fmt(e.undertime_deduction || 0)}" style="color:var(--red)" readonly></div>
      `);
      $('#dGross').text(fmt(e.total_gross));
      $('#dDeduct').text(fmt(e.total_deduct));
      $('#dNet').text(fmt(e.net_pay));
      $('#payheadDrawer').addClass('open');
    };

    // ── Payslip modal ────────────────────────────────────────────────────────
    window.showPayslip = function (id) {
      if (!payrollData) return;
      const e = payrollData.employees.find(x => x.id === id);
      if (!e) return;
      $('#ps_name').text(e.name);
      $('#ps_id').text(e.id);
      $('#ps_designation').text(e.designation);
      const pD = new Date();
      $('#ps_print_date').html(pD.toLocaleDateString('en-US') + '<br>' + pD.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }));
      $('#ps_issue_date').text(pD.toLocaleDateString('en-US'));
      $('#ps_month_label').text(`For the Period of ${payrollData.period}`);
      const rId = Math.floor(Math.random() * 900000) + 100000;
      $('#ps_print_id').text(rId);
      $('#ps_basic_full').html(pad(fmt(e.basic_salary).replace('₱', ''), 14));
      $('#ps_gross').html(pad(fmt(e.total_gross).replace('₱', ''), 14));
      let dhtml = [];
      const addD = (c, d, a) => {
        if (!a || parseFloat(a) === 0) return;
        dhtml.push(`<div style="display:flex; justify-content: space-between; margin-bottom:3px;"><span style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 5px;">${padRight(c, 4)} ${d}</span><span style="display:flex; flex: 2; gap: 10px; text-align: right;"><span style="width: 70px;">--</span><span style="width: 75px;">--</span><span style="width: 75px;">${pad(fmt(a).replace('₱', ''), 10)}</span></span></div>`);
      };
      addD('ABS', 'ABSENCE', e.absent_deduction);
      addD('TRD', 'TARDINESS', e.tardiness_deduction);
      addD('UND', 'UNDERTIME', e.undertime_deduction);
      addD('SSS', 'SSS PREMIUM', e.sss_ee);
      addD('PHIC', 'PHILHEALTH', e.philhealth_ee);
      addD('HDMF', 'PAG-IBIG FUND', e.pagibig_ee);
      addD('BIR', 'WITHHOLDING TAX', e.withholding_tax);
      addD('OTH', 'OTHER DEDUCTIONS', e.other_deductions);
      $('#ps_deductions_list').html(dhtml.join(''));
      $('#ps_total_deduct').html(pad(fmt(e.total_deduct).replace('₱', ''), 14));
      $('#ps_net').html(pad(fmt(e.net_pay).replace('₱', ''), 14));
      const h1 = Math.floor(e.net_pay / 2 * 100) / 100;
      const h2 = (e.net_pay - h1).toFixed(2);
      $('#ps_half_net1').html(pad(fmt(h1).replace('₱', ''), 14));
      $('#ps_half_net2').html(pad(fmt(h2).replace('₱', ''), 14));
      $('#payslipModal').addClass('open');
    };

    window.printAdminPayslip = function () {
      const prt = document.getElementById("payslipContent");
      const ctrl = document.getElementById("payslipHeaderControls");
      if (ctrl) ctrl.style.display = 'none';
      const WinPrint = window.open('', '', 'left=0,top=0,width=850,height=900,toolbar=0,scrollbars=0,status=0');
      WinPrint.document.write('<html><head><style>@page { size: portrait; margin: 10mm; } body { background: #fff; line-height: 1.35; -webkit-print-color-adjust: exact; }</style></head><body>');
      WinPrint.document.write(prt.outerHTML.replace('max-height:88vh', 'max-height:none').replace('overflow-y:auto', 'overflow:visible'));
      WinPrint.document.write('</body></html>');
      WinPrint.document.close();
      WinPrint.focus();
      setTimeout(() => { WinPrint.print(); WinPrint.close(); if (ctrl) ctrl.style.display = 'flex'; }, 500);
    };

    $('#closePayslip').on('click', () => $('#payslipModal').removeClass('open'));
    $('#payslipModal').on('click', function (e) { if (e.target === this) $(this).removeClass('open'); });
    $('#hideDrawer').on('click', () => $('#payheadDrawer').removeClass('open'));
    $('.ftab').on('click', function () { $('.ftab').removeClass('active'); $(this).addClass('active'); activeTab = $(this).text().trim().toLowerCase(); renderDocList(); });

    $('#btnApprove').on('click', async function () {
      if (!confirm('Are you certain you wish to approve this payroll?')) return;
      try {
        await fetch(API_RUNS + '/' + activeKey + '/status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: 'Approved' }) });
        loadRuns();
      } catch (e) { alert('Error approving record.'); }
    });

    $('#btnReject').on('click', async function () {
      const remarks = prompt('Enter rejection reason:');
      if (remarks === null) return;
      try {
        await fetch(API_RUNS + '/' + activeKey + '/status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: 'Rejected', remarks: remarks.trim() || 'No remarks provided.' }) });
        loadRuns();
      } catch (e) { alert('Error rejecting record.'); }
    });

    loadRuns();
  })();
</script>"""
    
    # We replace from start_idx to the end of the file
    content = content[:start_idx] + new_content
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("payroll_approval.html fixed")

if __name__ == "__main__":
    fix_payroll()
    fix_payroll_approval()
