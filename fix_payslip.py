import re

# 1. Cleanly extract full payslipContent from mypayslip.html
with open('pages/mypayslip.html', 'r', encoding='utf-8') as f:
    orig = f.read()

start_marker = '<div id="payslipContent"'
end_marker = '</script>'
inner_slice = orig[orig.find(start_marker):orig.find(end_marker)]

# inner_slice now contains `<div id="payslipContent" ...> ... </div>\n</div>\n\n`
# The last </div> is ps-body. We can just take up to the second-to-last </div> which is payslipContent.
last_div_idx = inner_slice.rfind('</div>')
second_last_div_idx = inner_slice.rfind('</div>', 0, last_div_idx)

# Extracted perfectly:
full_payslip_content = inner_slice[:second_last_div_idx + 6]

# 2. Add controls inside payslipContent
controls_html = """
    <div id="payslipHeaderControls" style="position:absolute;top:20px;right:25px;display:flex;gap:8px; z-index: 50; font-family: sans-serif; font-weight: bold; text-transform: none;">
      <button onclick="printAdminPayslip()" style="background:#f1f5f9;border:1px solid #cbd5e1;border-radius:7px;padding:6px 12px;color:#0f172a;font-size:11px;cursor:pointer;display:flex;align-items:center;gap:5px;">
          Print
      </button>
      <button id="closePayslip" style="background:#fee2e2;border:1px solid #fecaca;border-radius:7px;padding:6px 12px;color:#991b1b;font-size:11px;cursor:pointer;">&times; Close</button>
    </div>
"""

full_payslip_content = full_payslip_content.replace('id="payslipContent"', 'id="payslipContent" style="position:relative; width: 850px; max-height:88vh; overflow-y:auto; border-radius:14px; box-shadow:0 24px 60px rgba(0,0,0,0.22); font-family: \'Courier New\', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 35px 25px 25px; box-sizing: border-box; text-transform: uppercase;"', 1)
full_payslip_content = full_payslip_content.replace('style="display:none; width: 850px; max-width: 100%; font-family: \'Courier New\', Courier, monospace; font-size: 11px; line-height: 1.35; color: #000; background: #fff; padding: 25px; box-sizing: border-box; text-transform: uppercase;"', '')
full_payslip_content = full_payslip_content.replace('<div style="display: flex; justify-content: space-between; margin-bottom: 25px;">', controls_html + '<div style="display: flex; justify-content: space-between; margin-bottom: 25px;">')

# The wrapper we need to construct:
# <div class="modal-overlay" id="payslipModal" style="z-index:3000;">
#   {full_payslip_content}
# </div> <!-- ends modal-overlay -->
# </div> <!-- ends .pr-page -->

full_modal_replacement = f"""<div class="modal-overlay" id="payslipModal" style="z-index:3000;">
{full_payslip_content}
  </div>
</div>
"""

for fname in ['pages/payroll.html', 'pages/payroll_approval.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the corrupted block:
    # It started replacing from <div class="modal-overlay" id="payslipModal" style="z-index:3000;">
    search_start = '<div class="modal-overlay" id="payslipModal" style="z-index:3000;">'
    start_idx = content.find(search_start)
    
    if start_idx == -1:
        print(f"FAILED on {fname}")
        continue
    
    # We replace everything from start_idx up to `<script>`
    # Because my corrupted replace ate everything up to `<script>`
    script_idx = content.find('<script>', start_idx)
    
    if script_idx != -1:
        new_c = content[:start_idx] + full_modal_replacement + "\n" + content[script_idx:]
    else:
        new_c = content[:start_idx] + full_modal_replacement + "\n<script>\n"

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_c)

print("Patch complete.")
