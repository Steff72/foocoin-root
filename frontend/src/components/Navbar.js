import React from 'react'
import { Link } from 'react-router-dom'

import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'

import logo from '../assets/logo.png'


const MyNavbar = () => {

    return (
        <Container>
            <Navbar fixed="top" collapseOnSelect expand="md" bg="dark" variant="dark" className="Navbar">
                <Link to="/">
                    <Navbar.Brand className="ml-5">
                        <img
                            alt=""
                            src={logo}
                            width="40"
                            height="40"
                            className="d-inline-block align-botton mr-3"
                        />FooCoin
                    </Navbar.Brand>
                </Link>
            
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="ml-auto mr-5">
                    <Nav.Link href="/blockchain">FooChain</Nav.Link>
                    <Nav.Link href="/transactions">Open Tx Pool</Nav.Link>
                </Nav>
                </Navbar.Collapse>
            </Navbar>
        </Container>
    )
}

export default MyNavbar