import React from 'react'

import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'


const Header = () => {
    return (
        <Container>
            <Navbar fixed="top" className="Header justify-content-center">
                <h2>FooCoin</h2>
            </Navbar>
        </Container>
    )
}

export default Header