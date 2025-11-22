// 在 handleLogin 函式中 const handleLogin = async () => { loadingStore.setLoading(true,
'系統登入中...') try { await new Promise(resolve => setTimeout(resolve, 800)) if (form.username ===
'admin') { console.log('後台登入成功') // 1. 設定身分 roleStore.loginAsAdmin() // 2.
【修正重點】導航至後台儀表板 router.push({ name: 'BCMSDashboard' }) } else { alert('帳號或密碼錯誤
(測試帳號: admin)') } } catch (error) { console.error(error) alert('登入失敗') } finally {
loadingStore.setLoading(false) } }
