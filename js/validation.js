export function sanitize(value) { return String(value ?? '').replace(/[<>]/g, '').trim(); }
export function validateApplication(data) { if (!data.name || !data.service) return 'Please complete all required fields.'; if (!/^[6-9]\d{9}$/.test(data.mobile)) return 'Enter a valid 10-digit Indian mobile number.'; return ''; }
