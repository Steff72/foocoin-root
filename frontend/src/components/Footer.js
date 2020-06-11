import React from 'react'

import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'


const Footer = () => {
    const year = new Date().getFullYear()

    return (
        <Container>
            <Navbar fixed="bottom" bg="dark" className="Footer justify-content-center">
            Copyright &copy;
            <span>{year}</span> &nbsp;
            FooCoin
            </Navbar>
        </Container>
    )
}

export default Footer