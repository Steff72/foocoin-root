import React from 'react'

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import MyNavbar from './Navbar'
import Footer from './Footer'
import WalletInfo from './WalletInfo'
import SendTx from './SendTx'


const App = () => {
  return (
    <div className="App">
      <MyNavbar />
      <Container>
        <Row>
          <Col md={4}>
            <WalletInfo />
          </Col>
          <Col md={8}>
            <SendTx />
          </Col>
        </Row>
      </Container>
      <Footer />
    </div>
  );
}

export default App;
