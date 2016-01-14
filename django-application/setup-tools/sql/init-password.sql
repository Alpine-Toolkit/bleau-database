-- password fabricebleau
\connect bleaudb
UPDATE auth_user SET password='pbkdf2_sha256$24000$pp8dV2vNmdMV$IgWibdB0wzIRkGRKJJkFvi4d3NLbV/iGWwfdeeAHxTI=' where username='fabrice';
-- end
