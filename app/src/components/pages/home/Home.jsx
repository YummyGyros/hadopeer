import React from "react";
import "./home.css";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconeButton from '@mui/material/IconButton';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Box } from "@mui/material";

export default function Home() {
    return (
        <Container maxWidth="xl" className="home">
            <div className="homeTitle">HadoPeer</div>
            <Divider variant="inset" />
            <Box marginTop={9}>
                <Typography variant="h4" align="left">
                    Introduction
                </Typography>
                <Typography variant="h6" align="left">
                    Texte de présentation du projet avec une chronologie rapide
                    de la loi et de ses développements (texte rédigé par Marie
                    Puren). 
                </Typography>
                
                <Typography marginTop={5} variant="h4" align="left">
                    Équipe
                </Typography>
                <Typography marginTop={2} variant="h6" align="left">
                    Projet à l'initiative de Marie Puren, historienne du LabResearch d’Epitech Paris: recherche@epitech.eu
                    <br/>
                    <br/>
                    Développeurs d'Epitech Paris:
                    <br/>
                    <IconeButton target="_blank" rel="noreferrer noopener" href="https://github.com/jack-a-dit">
                    Adrien Mallet
                    </IconeButton>
                    - Scrapping, NLP - adrien.mallet.adh@gmail.com
                    <br/>
                    <IconeButton target="_blank" rel="noreferrer noopener" href="https://github.com/MTheboul">
                    Matteo Theboul
                    </IconeButton>
                    - Scrapping, Front-end - m.theboul.pro@gmail.com
                    <br/>
                    <IconeButton target="_blank" rel="noreferrer noopener" href="https://github.com/YummyGyros">
                    Robin Levavasseur
                    </IconeButton>
                    - Lead dev, Back-end - rlevavasseur.pro@gmail.com
                </Typography>
                <Typography marginTop={5} variant="h4" align="left">
                    Liens 
                </Typography>
                <Typography marginTop={2} variant="h6" align="left">
                <IconeButton target="_blank" rel="noreferrer noopener" href='https://github.com/YummyGyros/hadopeer-scrapped-data'>
                    Jeux de données
                </IconeButton>
                    <br/>
                    <IconeButton target="_blank" rel="noreferrer noopener" href='https://github.com/YummyGyros/hadopeer'>GitHub<GitHubIcon/></IconeButton>
                </Typography>
                <Typography marginTop={5} variant="h4" align="left">
                    Sources
                </Typography>
                <Typography marginTop={2} marginBottom={15} variant="h6" align="left">
                    <IconeButton target="_blank" rel="noreferrer noopener" href="http://www.senat.fr/dossier-legislatif/pjl07-405.html">
                        Sénat
                    </IconeButton>
                    <br/>
                    <IconeButton target="_blank" rel="noreferrer noopener" href="https://www.assemblee-nationale.fr/13/dossiers/internet.asp">
                        Assemblée Nationale
                    </IconeButton>
                </Typography>
            </Box>
            <a target="_blank" rel="noreferrer noopener" href="https://www.flaticon.com/free-icons/senate" title="senate icons">Senate icons created by Freepik - Flaticon</a>
        </Container>
        
    );
}
