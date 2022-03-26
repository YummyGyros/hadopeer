import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import { Link } from "react-router-dom";
import Button from "@mui/material/Button";

const pages = ["Chronologie", "Participants", "votes", "Analyse"];

const ResponsiveAppBar = (props) => {
    return (
        <AppBar color="primary">
            <Toolbar>
                <Link
                    to="/"
                    style={{
                        font: "italic small-caps bold 32px sans-serif",
                        textDecoration: "none",
                        color: "white",
                    }}
                >
                    HadoPeer
                </Link>
                <Box
                    sx={{
                        pl: 4,
                        flexGrow: 1,
                        display: { xs: "none", md: "flex" },
                    }}
                >
                    {pages.map((page) => (
                        <Button
                            key={page}
                            href={page}
                            variant={"raised"}
                            sx={{
                                my: 2,
                                color: "white",
                                display: "block",
                            }}
                        >
                            {page}
                        </Button>
                    ))}
                </Box>
            </Toolbar>
        </AppBar>
    );
};
export default ResponsiveAppBar;
