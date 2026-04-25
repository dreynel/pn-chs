import re

with open('pages/mypayslip.html', 'r', encoding='utf-8') as f:
    ms_txt = f.read()

# Extract DepEd HTML section
html_match = re.search(r'<div id="payslipContent".*?</div>\s*</div>', ms_txt, re.DOTALL)
deped_html = html_match.group(0)

# Add admin buttons inside the payslipContent
controls_html = """
    <div id="payslipHeaderControls" style="position:absolute;top:20px;right:25px;display:flex;gap:8px; z-index: 50; font-family: sans-serif; font-weight: bold; text-transform: none;">
      <button onclick="printAdminPayslip()" style="background:#f1f5f9;border:1px solid #cbd5e1;border-radius:7px;padding:6px 12px;color:#0f172a;font-size:11px;cursor:pointer;display:flex;align-items:center;gap:5px;">
          Print
      </button>
      <button id="closePayslip" style="background:#fee2e2;border:1px solid #fecaca;border-radius:7px;padding:6px 12px;color:#991b1b;font-size:11px;cursor:pointer;">&times; Close</button>
    </div>
"""
deped_html = deped_html.replace('id="payslipContent"', 'id="payslipContent" style="position:relative; width: 850px; max-height:88vh; overflow-y:auto; border-radius:14px; box-shadow:0 24px 60px rgba(0,0,0,0.22); font-family: \'Courier New\', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 35px 25px 25px; box-sizing: border-box; text-transform: uppercase;"', 1)

deped_html = deped_html.replace('style="display:none; width: 850px; max-width: 100%; font-family: \'Courier New\', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 25px; box-sizing: border-box; text-transform: uppercase;"', '') # cleanup if needed
deped_html = deped_html.replace('<div style="display: flex; justify-content: space-between; margin-bottom: 25px;">', controls_html + '<div style="display: flex; justify-content: space-between; margin-bottom: 25px;">')



js_snippet = """
  // ── Helpers ────────────────────────────────────────────────────────
  function fmt(n) { return parseFloat(n).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2}); }
  function pad(str, len) { str = String(str); while (str.length < len) str = '&nbsp;' + str; return str; }
  function padRight(str, len) { str = String(str); while (str.length < len) str = str + '&nbsp;'; return str; }

  // ── Payslip modal ────────────────────────────────────────────────────────
  window.showPayslip = function(id) {
    if (!payrollData) return;
    const e = payrollData.employees.find(x => x.id === id);
    if (!e) return;

    $('#ps_name').text(e.name);
    $('#ps_id').text(e.id);
    $('#ps_designation').text(e.designation);
    
    const pD = new Date();
    $('#ps_print_date').html(pD.toLocaleDateString('en-US') + '<br>' + pD.toLocaleTimeString('en-US', {hour12:false, hour:'2-digit', minute:'2-digit'}));
    $('#ps_issue_date').text(pD.toLocaleDateString('en-US'));
    $('#ps_month_label').text(`For the Period of ${payrollData.period}`);
    
    const rId = Math.floor(Math.random() * 900000) + 100000;
    $('#ps_print_id').text(rId);

    $('#ps_basic_full').html(pad(fmt(e.basic_salary), 14));
    $('#ps_gross').html(pad(fmt(e.total_gross), 14));

    let dhtml = [];
    function addDeduct(code, desc, amt) {
        if(!amt || parseFloat(amt) === 0) return;
        dhtml.push(`
          <div style="display:flex; justify-content: space-between; margin-bottom:3px;">
            <span style="flex: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-right: 5px;">${padRight(code, 4)} ${desc}</span>
            <span style="display:flex; flex: 2; gap: 10px; text-align: right;">
              <span style="width: 70px;">--</span>
              <span style="width: 75px;">--</span>
              <span style="width: 75px;">${pad(fmt(amt), 10)}</span>
            </span>
          </div>
        `);
    }

    addDeduct('ABS', 'ABSENCE', e.absent_deduction);
    addDeduct('TRD', 'TARDINESS', e.tardiness_deduction);
    addDeduct('UND', 'UNDERTIME', e.undertime_deduction);
    addDeduct('SSS', 'SSS PREMIUM', e.sss_ee);
    addDeduct('PHIC', 'PHILHEALTH', e.philhealth_ee);
    addDeduct('HDMF', 'PAG-IBIG FUND', e.pagibig_ee);
    addDeduct('BIR', 'WITHHOLDING TAX', e.withholding_tax);
    addDeduct('OTH', 'OTHER DEDUCTIONS', e.other_deductions);
    
    $('#ps_deductions_list').html(dhtml.join(''));

    $('#ps_total_deduct').html(pad(fmt(e.total_deduct), 14));
    $('#ps_net').html(pad(fmt(e.net_pay), 14));
    
    const half1 = Math.floor(e.net_pay / 2 * 100) / 100;
    const half2 = e.net_pay - half1;
    
    $('#ps_half_net1').html(pad(fmt(half1), 14));
    $('#ps_half_net2').html(pad(fmt(half2), 14));

    $('#payslipModal').addClass('open');
  };

  window.printAdminPayslip = function() {
    const prtContent = document.getElementById("payslipContent");
    const controls = document.getElementById("payslipHeaderControls");
    if(controls) controls.style.display = 'none';
    const WinPrint = window.open('', '', 'left=0,top=0,width=850,height=900,toolbar=0,scrollbars=0,status=0');
    WinPrint.document.write('<html><head><style>@page { size: portrait; margin: 10mm; } body { background: #fff; line-height: 1.35; -webkit-print-color-adjust: exact; }</style></head><body>');
    WinPrint.document.write(prtContent.outerHTML.replace('max-height: 88vh', 'max-height: none').replace('overflow-y: auto', 'overflow: visible'));
    WinPrint.document.write('</body></html>');
    WinPrint.document.close();
    WinPrint.focus();
    setTimeout(() => { 
      WinPrint.print(); 
      WinPrint.close(); 
      if(controls) controls.style.display = 'flex';
    }, 500);
  };
"""

for fname in ['pages/payroll.html', 'pages/payroll_approval.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace HTML Modal
    # The modal starts at <div class="modal-overlay" id="payslipModal" style="z-index:3000;">
    # and ends right before </div>\n\n</div>\n\n<script>
    import re
    # Remove old modal content inside payslipModal
    new_c = re.sub(r'(<div class="modal-overlay" id="payslipModal" style="z-index:3000;">).*?(?=</div>\s*</div>\s*<script>)', r'\1\n' + deped_html + '\n', content, flags=re.DOTALL)
    
    # Replace window.showPayslip
    new_c = re.sub(r'window\.showPayslip = function\(id\) \{.*?\};\n', js_snippet, new_c, flags=re.DOTALL)
    
    # Make sure we don't accidentally define fmt multiple times
    new_c = new_c.replace("function fmt(n) { return '₱' + parseFloat(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }", "")
    new_c = new_c.replace("function fmt(n) { return '₱' + parseFloat(n).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2}); }", "")

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_c)

print("Patch complete.")
