import React from 'react'

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import Header from './Header'
import Footer from './Footer'
import WalletInfo from './WalletInfo'
import SendTx from './SendTx'
import TxPool from './TxPool'
import Blockchain from './Blockchain'


const App = () => {
  return (
    <div className="App">
      <Header />
      <Container>
        <Row>
          <Col lg={4}>
            <WalletInfo />
          </Col>
          <Col lg={8}>
            <SendTx />
          </Col>
        </Row>
        <Row>
          <Col lg={4}>
            <TxPool />
          </Col>
          <Col lg={8}>
            <Blockchain />
          </Col>
        </Row>
      </Container>
      <Footer />
    </div>
  );
}

export default App;
