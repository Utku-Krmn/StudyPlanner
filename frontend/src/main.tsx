import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {CssBaseline,ThemeProvider,createTheme} from '@mui/material'
import App from './App'
const theme=createTheme({palette:{primary:{main:'#6C5CE7',dark:'#5541D7',light:'#EEEAFE'},secondary:{main:'#111827'},background:{default:'#F6F7FB',paper:'#fff'},text:{primary:'#172033',secondary:'#758096'},success:{main:'#18A978'},warning:{main:'#F59E62'}},shape:{borderRadius:14},typography:{fontFamily:'Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif',h1:{fontWeight:800,letterSpacing:'-.04em'},h2:{fontWeight:800,letterSpacing:'-.025em'},h3:{fontWeight:750,letterSpacing:'-.02em'},button:{fontWeight:750,textTransform:'none'}},components:{MuiButton:{styleOverrides:{root:{borderRadius:11,boxShadow:'none',paddingInline:18}}},MuiPaper:{styleOverrides:{root:{backgroundImage:'none'}}},MuiTextField:{defaultProps:{size:'small'}}}})
createRoot(document.getElementById('root')!).render(<StrictMode><ThemeProvider theme={theme}><CssBaseline/><App/></ThemeProvider></StrictMode>)
